# -*- coding: utf-8 -*-
import os
import sys
import logging
import asyncio

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from asgiref.sync import sync_to_async
from accounts.models import User, WorkerPortfolio, WorkerReview, UserFeedback
from categories.models import Category, Position
from locations.models import Region, reverse_geocode
from orders.models import JobPost, JobApplication
from bot_control.models import BotConfig

from telegram_client_bot.texts import t, TEXTS
from telegram import Bot
from telegram_client_bot.distribution import notify_matching_workers_about_job

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

logger = logging.getLogger(__name__)

# CLIENT BOT STATES
(
    STATE_AUTH_LANG,           # 0.1: Til tanlash
    STATE_AUTH_NAME,           # 0.2: Ism familiya
    STATE_AUTH_PHONE,          # 0.2: Telefon raqam
    STATE_MAIN_MENU,           # 0.3: Asosiy Menyu
    
    # E'lon berish qadamlari
    STATE_POST_EMP_TYPE,       # 1.1: Bandlik turi
    STATE_POST_CATEGORY,       # 1.2: Asosiy soha
    STATE_POST_POSITION,       # 1.3: Mutaxassislik
    STATE_POST_DESCRIPTION,    # 2.1: Ish tavsifi
    STATE_POST_PHOTO,          # 2.1: Rasm (ixtiyoriy)
    STATE_POST_WORKERS_COUNT,  # 2.2: Ishchilar soni
    STATE_POST_GENDER,         # 2.3: Jinsi talabi
    STATE_POST_START_TIME,     # 2.4: Boshlanish vaqti
    STATE_POST_CUSTOM_START,   # 2.4: Aniq sana kiritish
    STATE_POST_PRICE_TYPE,     # 2.5: To'lov turi
    STATE_POST_PRICE_AMOUNT,   # 2.5: To'lov summasi
    STATE_POST_LOCATION,       # 3.1: GPS Lokatsiya
    STATE_POST_MANUAL_REGION,  # 3.1: Viloyat tanlash
    STATE_POST_MANUAL_DISTRICT,# 3.1: Tuman tanlash
    STATE_POST_ADDRESS,        # 3.2: Aniq manzil / mo'ljal
    STATE_POST_REVIEW,         # 4: E'lonni tasdiqlash
    STATE_POST_CHANGE_PHONE,   # 4-alt: Boshqa raqam kiritish
    
    # Mening e'lonlarim
    STATE_MY_POSTS_VIEW,       # E'lonlarni ko'rish / boshqarish
    STATE_EDIT_PROFILE_NAME,   # Profil: Ism o'zgartirish
    STATE_EDIT_PROFILE_PHONE,  # Profil: Telefon o'zgartirish
    STATE_SUPPORT_FEEDBACK,    # Qo'llab-quvvatlash: Taklif / shikoyat kiritish
) = range(25)

PAGE_SIZE = 8

# ==================== DB HELPER ASYNC FUNCTIONS ====================

@sync_to_async
def create_client_feedback(telegram_id: int, message_text: str):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if user:
        return UserFeedback.objects.create(user=user, message=message_text)
    return None

@sync_to_async
def get_bot_support_info():
    config = BotConfig.get_config()
    return {
        'call_center_phone': config.call_center_phone or "+998 (71) 200-00-00"
    }

@sync_to_async
def get_client_user(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None
    is_fully_complete = bool(
        user.is_registered and 
        user.phone_number and 
        user.first_name and 
        not user.needs_profile_update
    )
    return {
        'id': user.id,
        'telegram_id': user.telegram_id,
        'first_name': user.first_name,
        'phone_number': user.phone_number,
        'language': user.language or 'uz',
        'is_registered': is_fully_complete,
        'role': user.role,
        'needs_profile_update': user.needs_profile_update,
        'profile_update_reason': user.profile_update_reason,
    }

@sync_to_async
def save_or_update_client_profile(telegram_id: int, username: str, data: dict):
    user, _ = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'username': username or f"tg_client_{telegram_id}",
            'role': User.Role.CLIENT,
            'started_client_bot': True,
        }
    )
    user.started_client_bot = True
    if data.get('lang'):
        user.language = data['lang']
    if data.get('name'):
        user.first_name = data['name']
    if data.get('phone'):
        user.phone_number = data['phone']
    user.is_registered = True
    user.needs_profile_update = False
    user.profile_update_reason = ''
    user.save()
    return user

@sync_to_async
def get_all_client_users_for_notification():
    return list(User.objects.filter(
        telegram_id__isnull=False,
        started_client_bot=True
    ).values('telegram_id', 'language'))

@sync_to_async
def get_active_categories():
    return list(Category.objects.filter(is_active=True).order_by('order', 'id').values('id', 'name_uz', 'name_oz', 'name_ru', 'name_en', 'icon'))

@sync_to_async
def get_positions_by_category(category_id: int):
    return list(Position.objects.filter(category_id=category_id, is_active=True).order_by('order', 'id').values('id', 'name_uz', 'name_oz', 'name_ru', 'name_en'))

@sync_to_async
def get_all_regions():
    return list(Region.objects.filter(is_active=True).order_by('order', 'id').values('id', 'name_uz', 'name_oz', 'name_ru', 'name_en'))

@sync_to_async
def save_job_post_to_db(telegram_id: int, post_data: dict):
    user = User.objects.get(telegram_id=telegram_id)
    job = JobPost.objects.create(
        employer=user,
        employment_type=post_data.get('employment_type', 'daily'),
        category_id=post_data.get('category_id'),
        position_id=post_data.get('position_id'),
        custom_position_name=post_data.get('custom_position_name'),
        description=post_data.get('description', ''),
        photo_file_id=post_data.get('photo_file_id'),
        workers_count=post_data.get('workers_count', '1 nafar'),
        gender_requirement=post_data.get('gender_requirement', 'any'),
        start_time_type=post_data.get('start_time_type', 'urgent'),
        custom_start_date=post_data.get('custom_start_date'),
        is_price_negotiable=post_data.get('is_price_negotiable', True),
        price_amount=post_data.get('price_amount'),
        region_id=post_data.get('region_id'),
        district=post_data.get('district'),
        address=post_data.get('address'),
        latitude=post_data.get('latitude'),
        longitude=post_data.get('longitude'),
        contact_name=post_data.get('contact_name') or user.first_name,
        contact_phone=post_data.get('contact_phone') or user.phone_number,
        contact_telegram_username=user.username,
        status=JobPost.Status.ACTIVE
    )
    return job.id

@sync_to_async
def get_employer_job_posts(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return []
    return list(JobPost.objects.filter(employer=user).select_related('category', 'position', 'region').order_by('-created_at')[:20])

@sync_to_async
def get_employer_applications(telegram_id: int, post_id: int = None):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return []
    qs = JobApplication.objects.filter(job_post__employer=user, is_deleted_by_employer=False)
    if post_id:
        qs = qs.filter(job_post_id=post_id)
    return list(qs.select_related('job_post', 'worker', 'job_post__position', 'job_post__category', 'job_post__region').order_by('-applied_at')[:30])

@sync_to_async
def get_application_details_in_db(app_id: int):
    app = JobApplication.objects.select_related(
        'job_post', 'worker', 'job_post__employer', 'job_post__position', 'job_post__category', 'job_post__region'
    ).filter(id=app_id).first()
    if not app:
        return None
    worker = app.worker
    positions = list(worker.selected_positions.values_list('name_uz', flat=True))
    if not positions and worker.position:
        positions = [worker.position.name_uz]
    
    reviews_count = worker.received_reviews.count()
    completed_count = worker.completed_jobs_count
    
    portfolio_photos = list(worker.portfolio_items.all()[:5].values('file_id', 'caption'))

    return {
        'id': app.id,
        'status': app.status,
        'applied_at': app.applied_at.strftime("%d.%m.%Y %H:%M") if app.applied_at else "",
        'proposal_message': app.proposal_message or "Taklif xabari kiritilmagan",
        'job_id': app.job_post.id,
        'job_title': app.job_post.position.name_uz if app.job_post.position else (app.job_post.custom_position_name or 'Ish'),
        'job_status': app.job_post.status,
        'job_address': f"{app.job_post.region.name if app.job_post.region else ''} {app.job_post.district or ''} {app.job_post.address or ''}".strip(),
        'employer_id': app.job_post.employer.id,
        'employer_name': app.job_post.contact_name or app.job_post.employer.first_name,
        'employer_phone': app.job_post.contact_phone or app.job_post.employer.phone_number,
        'employer_tg_username': app.job_post.contact_telegram_username or app.job_post.employer.username or '',
        'employer_tg_id': app.job_post.employer.telegram_id,
        'worker_id': worker.id,
        'worker_tg_id': worker.telegram_id,
        'worker_name': worker.get_full_name() or worker.first_name or 'Usta',
        'worker_phone': worker.phone_number or "Ko'rsatilmagan",
        'worker_tg_username': worker.username or '',
        'worker_age': worker.age or 'Ko\'rsatilmagan',
        'worker_gender': worker.get_gender_display() if worker.gender else 'Ko\'rsatilmagan',
        'worker_rating': worker.rating or 5.0,
        'worker_reviews_count': reviews_count,
        'worker_completed_count': completed_count,
        'worker_positions': ", ".join(positions) if positions else 'Mutaxassis',
        'worker_location': f"{worker.region.name if worker.region else ''} {worker.district or ''}".strip() or "Ko'rsatilmagan",
        'portfolio_photos': portfolio_photos
    }

@sync_to_async
def hire_worker_for_job_in_db(app_id: int):
    app = JobApplication.objects.select_related('job_post', 'worker', 'job_post__employer').filter(id=app_id).first()
    if not app:
        return False, "Arizachi topilmadi", None
        
    job = app.job_post
    if job.status == JobPost.Status.COMPLETED:
        return False, "Ushbu e'longa allaqachon ishchi qabul qilingan va yopilgan!", None
        
    app.status = JobApplication.Status.ACCEPTED
    app.is_deleted_by_worker = False  # Resurface in worker's applications list if previously soft-deleted
    app.save(update_fields=['status', 'is_deleted_by_worker'])
    
    # Mark job completed
    job.status = JobPost.Status.COMPLETED
    job.save(update_fields=['status'])
    
    # Reject other applications
    JobApplication.objects.filter(job_post=job).exclude(id=app.id).update(status=JobApplication.Status.REJECTED)
    
    worker = app.worker
    employer = job.employer
    
    return True, "Ishchi muvaffaqiyatli qabul qilindi!", {
        'app_id': app.id,
        'job_id': job.id,
        'job_title': job.position.name_uz if job.position else (job.custom_position_name or 'Ish'),
        'job_address': f"{job.region.name if job.region else ''} {job.district or ''} {job.address or ''}".strip(),
        'employer_tg_id': employer.telegram_id,
        'employer_name': job.contact_name or employer.first_name,
        'employer_phone': job.contact_phone or employer.phone_number or "Ko'rsatilmagan",
        'employer_username': job.contact_telegram_username or employer.username or '',
        'worker_tg_id': worker.telegram_id,
        'worker_name': worker.get_full_name() or worker.first_name,
        'worker_phone': worker.phone_number or "Ko'rsatilmagan",
        'worker_username': worker.username or ''
    }

@sync_to_async
def update_job_post_status(job_id: int, new_status: str):
    JobPost.objects.filter(id=job_id).update(status=new_status)

@sync_to_async
def delete_job_post(job_id: int):
    JobPost.objects.filter(id=job_id).delete()

@sync_to_async
def delete_job_application_in_db(app_id: int, employer_tg_id: int):
    app = JobApplication.objects.filter(id=app_id, job_post__employer__telegram_id=employer_tg_id).first()
    if app:
        app.is_deleted_by_employer = True
        app.save(update_fields=['is_deleted_by_employer'])
        return True
    return False

# ==================== HANDLERS: START & AUTH ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    user_data = context.user_data
    user_data.clear()

    # 1. Deep-link orqali kirgan bo'lsa (masalan: /start ref_worker_bot_12345_uz)
    args = context.args
    deep_lang = None
    if args and len(args) > 0:
        arg = args[0]
        if 'ref_worker_bot' in arg:
            parts = arg.split('_')
            if len(parts) >= 4 and parts[-1] in ['uz', 'oz', 'ru', 'en']:
                deep_lang = parts[-1]

    client = await get_client_user(tg_id)
    if client and client['is_registered']:
        lang = client['language'] or 'uz'
        if deep_lang:
            lang = deep_lang
            await save_or_update_client_profile(tg_id, update.effective_user.username, {'lang': lang})
        user_data['lang'] = lang
        user_data['name'] = client['first_name']
        user_data['phone'] = client['phone_number']
        return await show_main_menu(update, context)

    if deep_lang:
        user_data['lang'] = deep_lang
        text = t('welcome_employer', deep_lang, name=update.effective_user.first_name or 'Foydalanuvchi')
        text += "\n\n" + t('step0_name_title', deep_lang)
        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(text=text, parse_mode='HTML')
        else:
            await update.message.reply_text(text=text, parse_mode='HTML')
        return STATE_AUTH_NAME

    # Til tanlash tugmalari
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O‘zbekcha (Lotin)", callback_data="lang_uz"),
            InlineKeyboardButton("🇺🇿 Ўзбекча (Крилл)", callback_data="lang_oz"),
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg_text = "Assalomu alaykum! <b>ISH JOYLASH BOTI</b>ga xush kelibsiz!\n\nIltimos, muloqot tilini tanlang:\nПожалуйста, выберите язык:\nPlease select your language:"
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=msg_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(text=msg_text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_AUTH_LANG

async def auth_lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    lang = data.replace('lang_', '')
    context.user_data['lang'] = lang
    
    text = t('lang_selected', lang) + "\n\n" + t('step0_name_title', lang)
    await query.edit_message_text(text=text, parse_mode='HTML')
    return STATE_AUTH_NAME

async def auth_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    lang = context.user_data.get('lang', 'uz')
    
    if len(name) < 2:
        await update.message.reply_text("⚠️ Iltimos, ismingizni to'liq kiriting:")
        return STATE_AUTH_NAME
        
    context.user_data['name'] = name
    
    keyboard = [
        [KeyboardButton(t('btn_send_phone', lang), request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        t('step0_phone_title', lang),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_AUTH_PHONE

async def auth_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    phone = ''
    
    if update.message.contact:
        phone = update.message.contact.phone_number
    elif update.message.text:
        text_val = update.message.text.strip()
        cleaned = text_val.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if cleaned.startswith('+') and len(cleaned) >= 9 and cleaned[1:].isdigit():
            phone = cleaned
        elif cleaned.startswith('998') and len(cleaned) == 12 and cleaned.isdigit():
            phone = '+' + cleaned
        elif len(cleaned) == 9 and cleaned.isdigit():
            phone = '+998' + cleaned

    if not phone:
        await update.message.reply_text(t('phone_invalid', lang), parse_mode='HTML')
        return STATE_AUTH_PHONE

    if not phone.startswith('+'):
        phone = '+' + phone

    context.user_data['phone'] = phone
    tg_id = update.effective_user.id
    username = update.effective_user.username
    
    await save_or_update_client_profile(tg_id, username, context.user_data)
    
    # Remove reply keyboard
    await update.message.reply_text(
        "✅ Profilingiz muvaffaqiyatli saqlandi!",
        reply_markup=ReplyKeyboardRemove()
    )
    return await show_main_menu(update, context)

# ==================== MAIN MENU & DASHBOARD ====================

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    name = context.user_data.get('name') or update.effective_user.first_name or 'Mijoz'
    phone = context.user_data.get('phone') or 'Kiritilgan'
    
    posts = await get_employer_job_posts(update.effective_user.id)
    active_count = len([p for p in posts if p.status == JobPost.Status.ACTIVE])
    
    apps = await get_employer_applications(update.effective_user.id)
    apps_count = len(apps)
    apps_badge = f" ({apps_count})" if apps_count > 0 else ""
    
    text = t('main_menu', lang, name=name, phone=phone, active_posts_count=active_count)
    
    try:
        worker_bot_url = await sync_to_async(BotConfig.get_worker_bot_link)()
    except Exception as e:
        logger.error(f"Error getting worker_bot_link: {e}")
        worker_bot_url = "https://t.me/ish_24_7_bot?start=ref_client_bot"

    keyboard = [
        [InlineKeyboardButton(t('btn_menu_new_post', lang), callback_data="menu_new_post")],
        [
            InlineKeyboardButton(t('btn_menu_my_posts', lang) + f" ({len(posts)})", callback_data="menu_my_posts"),
            InlineKeyboardButton(t('btn_menu_applications', lang) + apps_badge, callback_data="menu_applications"),
        ],
        [
            InlineKeyboardButton(t('btn_menu_profile', lang), callback_data="menu_profile"),
            InlineKeyboardButton(t('btn_menu_settings', lang), callback_data="menu_settings"),
        ],
        [
            InlineKeyboardButton(t('btn_menu_help', lang), callback_data="menu_help"),
            InlineKeyboardButton(t('btn_menu_switch_bot', lang), url=worker_bot_url),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU

# ==================== POST JOB FLOW ====================

async def start_job_post_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    context.user_data['job_post'] = {}
    
    # 1.1 Bandlik turi
    keyboard = [
        [InlineKeyboardButton(t('emp_type_daily', lang), callback_data="emp_type_daily")],
        [InlineKeyboardButton(t('emp_type_permanent', lang), callback_data="emp_type_permanent")],
        [InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=t('step1_emp_type_title', lang),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_POST_EMP_TYPE

async def post_emp_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    if data == "back_to_main_menu":
        return await show_main_menu(update, context)
        
    emp_type = 'daily' if 'daily' in data else 'permanent'
    context.user_data['job_post']['employment_type'] = emp_type
    
    return await render_categories_page(query, context, page=0)

async def render_categories_page(query, context, page=0):
    lang = context.user_data.get('lang', 'uz')
    categories = await get_active_categories()
    
    total_pages = max(1, (len(categories) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))
    
    start_idx = page * PAGE_SIZE
    page_cats = categories[start_idx:start_idx + PAGE_SIZE]
    
    keyboard = []
    for cat in page_cats:
        c_name = cat.get(f'name_{lang}') or cat['name_uz']
        icon = cat.get('icon') or '🛠️'
        keyboard.append([InlineKeyboardButton(f"{icon} {c_name}", callback_data=f"cat_{cat['id']}")])
        
    nav_btns = []
    if page > 0:
        nav_btns.append(InlineKeyboardButton("⬅️", callback_data=f"catpage_{page-1}"))
    if page < total_pages - 1:
        nav_btns.append(InlineKeyboardButton("➡️", callback_data=f"catpage_{page+1}"))
    if nav_btns:
        keyboard.append(nav_btns)
        
    keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_emp_type")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=t('step1_cat_title', lang, current=page+1, total=total_pages),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_POST_CATEGORY

async def post_category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    if data == "back_to_emp_type":
        return await start_job_post_flow(update, context)
    if data.startswith("catpage_"):
        p = int(data.split('_')[1])
        return await render_categories_page(query, context, page=p)
        
    cat_id = int(data.split('_')[1])
    context.user_data['job_post']['category_id'] = cat_id
    
    return await render_positions_page(query, context, category_id=cat_id, page=0)

async def render_positions_page(query, context, category_id, page=0):
    lang = context.user_data.get('lang', 'uz')
    positions = await get_positions_by_category(category_id)
    
    if not positions:
        context.user_data['job_post']['position_id'] = None
        await query.edit_message_text(text=t('step2_desc_title', lang), parse_mode='HTML')
        return STATE_POST_DESCRIPTION

    total_pages = max(1, (len(positions) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))
    
    start_idx = page * PAGE_SIZE
    page_pos = positions[start_idx:start_idx + PAGE_SIZE]
    
    keyboard = []
    for pos in page_pos:
        p_name = pos.get(f'name_{lang}') or pos['name_uz']
        keyboard.append([InlineKeyboardButton(f"🔨 {p_name}", callback_data=f"pos_{pos['id']}")])
        
    nav_btns = []
    if page > 0:
        nav_btns.append(InlineKeyboardButton("⬅️", callback_data=f"pospage_{page-1}"))
    if page < total_pages - 1:
        nav_btns.append(InlineKeyboardButton("➡️", callback_data=f"pospage_{page+1}"))
    if nav_btns:
        keyboard.append(nav_btns)
        
    keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_categories")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=t('step1_pos_title', lang, current=page+1, total=total_pages),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_POST_POSITION

async def post_position_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    if data == "back_to_categories":
        return await render_categories_page(query, context, page=0)
    if data.startswith("pospage_"):
        p = int(data.split('_')[1])
        cat_id = context.user_data['job_post']['category_id']
        return await render_positions_page(query, context, category_id=cat_id, page=p)
        
    pos_id = int(data.split('_')[1])
    context.user_data['job_post']['position_id'] = pos_id
    
    await query.edit_message_text(text=t('step2_desc_title', lang), parse_mode='HTML')
    return STATE_POST_DESCRIPTION

async def post_description_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    desc = update.message.text.strip()
    lang = context.user_data.get('lang', 'uz')
    
    if len(desc) < 5:
        await update.message.reply_text("⚠️ Iltimos, ish tavsifini batafsilroq yozing:")
        return STATE_POST_DESCRIPTION
        
    context.user_data['job_post']['description'] = desc
    
    keyboard = [
        [InlineKeyboardButton(t('btn_skip', lang), callback_data="skip_photo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=t('step2_photo_title', lang),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_POST_PHOTO

async def post_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    
    if update.callback_query and update.callback_query.data == "skip_photo":
        await update.callback_query.answer()
        context.user_data['job_post']['photo_file_id'] = None
    elif update.message and update.message.photo:
        file_id = update.message.photo[-1].file_id
        context.user_data['job_post']['photo_file_id'] = file_id
    else:
        context.user_data['job_post']['photo_file_id'] = None
        
    return await ask_workers_count(update, context)

async def ask_workers_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    
    keyboard = [
        [
            InlineKeyboardButton(t('workers_1', lang), callback_data="wc_1 nafar"),
            InlineKeyboardButton(t('workers_2', lang), callback_data="wc_2 nafar"),
        ],
        [
            InlineKeyboardButton(t('workers_3_5', lang), callback_data="wc_3-5 nafar"),
            InlineKeyboardButton(t('workers_5_plus', lang), callback_data="wc_Katta brigada (5+)"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = t('step2_workers_count_title', lang)
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_POST_WORKERS_COUNT

async def post_workers_count_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    context.user_data['job_post']['workers_count'] = data.replace('wc_', '')
    
    # 2.3 Jinsi
    keyboard = [
        [InlineKeyboardButton(t('gender_any', lang), callback_data="g_any")],
        [
            InlineKeyboardButton(t('gender_male', lang), callback_data="g_male"),
            InlineKeyboardButton(t('gender_female', lang), callback_data="g_female"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=t('step2_gender_title', lang),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_POST_GENDER

async def post_gender_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    context.user_data['job_post']['gender_requirement'] = data.replace('g_', '')
    
    # 2.4 Boshlanish vaqti
    keyboard = [
        [InlineKeyboardButton(t('start_urgent', lang), callback_data="st_urgent")],
        [InlineKeyboardButton(t('start_tomorrow', lang), callback_data="st_tomorrow")],
        [InlineKeyboardButton(t('start_custom', lang), callback_data="st_custom")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=t('step2_start_time_title', lang),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_POST_START_TIME

async def post_start_time_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    st_type = data.replace('st_', '')
    context.user_data['job_post']['start_time_type'] = st_type
    
    if st_type == 'custom':
        await query.edit_message_text(
            text="🗓 Ish boshlanadigan aniq sana va vaqtni kiriting:\n<i>(Masalan: 15-sentyabr, soat 08:30 da)</i>",
            parse_mode='HTML'
        )
        return STATE_POST_CUSTOM_START
        
    return await ask_price_step(query, context)

async def post_custom_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_val = update.message.text.strip()
    context.user_data['job_post']['custom_start_date'] = text_val
    return await ask_price_step(update, context)

async def ask_price_step(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    keyboard = [
        [InlineKeyboardButton(t('price_negotiable', lang), callback_data="pr_negotiable")],
        [InlineKeyboardButton(t('price_fixed_btn', lang), callback_data="pr_fixed")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = t('step2_price_title', lang)
    if hasattr(update_or_query, 'edit_message_text'):
        await update_or_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update_or_query.message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_POST_PRICE_TYPE

async def post_price_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    if data == "pr_negotiable":
        context.user_data['job_post']['is_price_negotiable'] = True
        context.user_data['job_post']['price_amount'] = None
        return await ask_location_step(query, context)
    else:
        context.user_data['job_post']['is_price_negotiable'] = False
        await query.edit_message_text(
            text=t('step2_enter_price_prompt', lang),
            parse_mode='HTML'
        )
        return STATE_POST_PRICE_AMOUNT

async def post_price_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text.strip()
    context.user_data['job_post']['price_amount'] = amount
    return await ask_location_step(update, context)

async def ask_location_step(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    
    keyboard = [
        [KeyboardButton(t('btn_send_gps', lang), request_location=True)],
        [KeyboardButton(t('btn_select_region_manually', lang))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    msg_text = t('step3_geo_title', lang)
    if hasattr(update_or_query, 'message') and update_or_query.message:
        await update_or_query.message.reply_text(text=msg_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update_or_query.reply_text(text=msg_text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_POST_LOCATION

async def post_location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    
    if update.message.location:
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        context.user_data['job_post']['latitude'] = lat
        context.user_data['job_post']['longitude'] = lon
        
        geo = await sync_to_async(reverse_geocode)(lat, lon)
        context.user_data['job_post']['region_id'] = geo.get('region_id')
        context.user_data['job_post']['district'] = geo.get('district', '')
        
        await update.message.reply_text(
            f"📍 Joylashuv aniqlandi: <b>{geo.get('region_name', '')} ({geo.get('district', '')})</b>\n\n" + t('step3_address_title', lang),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='HTML'
        )
        return STATE_POST_ADDRESS
    elif update.message.text and t('btn_select_region_manually', lang) in update.message.text:
        return await post_manual_region_start_handler(update, context)
    else:
        context.user_data['job_post']['district'] = update.message.text.strip()
        await update.message.reply_text(
            t('step3_address_title', lang),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='HTML'
        )
        return STATE_POST_ADDRESS

async def post_manual_region_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    reg_id = int(data.split('_')[1])
    region = await sync_to_async(lambda: Region.objects.filter(id=reg_id).first())()
    reg_name = region.get_name(lang) if region else "Tanlangan viloyat"
    
    context.user_data['job_post']['region_id'] = reg_id
    context.user_data['job_post']['region_name'] = reg_name
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Viloyatni qayta tanlash", callback_data="back_to_regions")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"🏛 Tanlandi: <b>{reg_name}</b>\n\nIltimos, tuman / shahar nomini yozib yuboring:\n<i>(Masalan: Chilonzor tumani yoki Samarqand shahri)</i>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_POST_MANUAL_DISTRICT

async def post_manual_district_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dist = update.message.text.strip()
    lang = context.user_data.get('lang', 'uz')
    context.user_data['job_post']['district'] = dist
    
    await update.message.reply_text(
        t('step3_address_title', lang),
        parse_mode='HTML'
    )
    return STATE_POST_ADDRESS

async def post_address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    addr = update.message.text.strip()
    context.user_data['job_post']['address'] = addr
    return await render_review_card(update, context)

async def render_review_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    job = context.user_data.get('job_post', {})
    
    emp_type_str = t('emp_type_daily', lang) if job.get('employment_type') == 'daily' else t('emp_type_permanent', lang)
    
    category = await sync_to_async(lambda: Category.objects.filter(id=job.get('category_id')).first())()
    position = await sync_to_async(lambda: Position.objects.filter(id=job.get('position_id')).first())() if job.get('position_id') else None
    
    title = position.name_uz if position else (category.name_uz if category else "Ish")
    
    gender_map = {'any': t('gender_any', lang), 'male': t('gender_male', lang), 'female': t('gender_female', lang)}
    gender_str = gender_map.get(job.get('gender_requirement', 'any'), "Farqi yo'q")
    
    start_map = {'urgent': t('start_urgent', lang), 'tomorrow': t('start_tomorrow', lang), 'custom': job.get('custom_start_date', 'Kelishilgan')}
    start_str = start_map.get(job.get('start_time_type', 'urgent'), 'Tezda')
    
    price_str = f"{job.get('price_amount')}" if (not job.get('is_price_negotiable') and job.get('price_amount')) else t('price_negotiable', lang)
    
    reg_name = job.get('region_name') or 'Hudud'
    dist_name = job.get('district') or ''
    
    contact_name = context.user_data.get('name') or update.effective_user.first_name
    contact_phone = context.user_data.get('phone') or 'Kiritilgan'
    
    card_text = t(
        'step4_review_title',
        lang,
        title=title,
        emp_type=emp_type_str,
        workers_count=job.get('workers_count', '1 nafar'),
        gender=gender_str,
        desc=job.get('description', ''),
        price=price_str,
        region=reg_name,
        district=dist_name,
        address=job.get('address', ''),
        start_time=start_str,
        contact_name=contact_name,
        contact_phone=contact_phone
    )
    
    keyboard = [
        [InlineKeyboardButton(t('btn_post_confirm', lang), callback_data="confirm_job_post")],
        [InlineKeyboardButton(t('btn_change_contact', lang), callback_data="change_post_contact")],
        [InlineKeyboardButton(t('btn_cancel_post', lang), callback_data="cancel_job_post")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if job.get('photo_file_id'):
        await update.message.reply_photo(
            photo=job['photo_file_id'],
            caption=card_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            text=card_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    return STATE_POST_REVIEW

async def post_review_action_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    if data == "confirm_job_post":
        job_post_data = context.user_data.get('job_post', {})
        tg_id = update.effective_user.id
        
        job_id = await save_job_post_to_db(tg_id, job_post_data)
        
        # Push-xabarnoma tarqatish
        asyncio.create_task(notify_matching_workers_about_job(job_id))
        
        await query.edit_message_caption(caption=t('post_success', lang), parse_mode='HTML') if query.message.photo else await query.edit_message_text(text=t('post_success', lang), parse_mode='HTML')
        
        await asyncio.sleep(1.5)
        return await show_main_menu(update, context)
        
    elif data == "change_post_contact":
        await query.message.reply_text("📞 Aloqa uchun boshqa telefon raqamini kiriting (+998XXXXXXXXX):")
        return STATE_POST_CHANGE_PHONE
        
    elif data == "cancel_job_post":
        context.user_data.pop('job_post', None)
        return await show_main_menu(update, context)

async def post_change_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    context.user_data['job_post']['contact_phone'] = phone
    return await render_review_card(update, context)

# ==================== MY POSTS & APPLICATIONS ====================

async def my_posts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    posts = await get_employer_job_posts(update.effective_user.id)
    if not posts:
        keyboard = [[InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_main_menu")]]
        await query.edit_message_text(
            text=t('my_posts_empty', lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return STATE_MAIN_MENU

    keyboard = []
    for p in posts:
        status_emoji = '🟢' if p.status == JobPost.Status.ACTIVE else ('⏸' if p.status == JobPost.Status.PAUSED else '✅')
        p_name = p.position.name_uz if p.position else (p.category.name_uz if p.category else 'Ish')
        keyboard.append([InlineKeyboardButton(f"{status_emoji} #{p.id}: {p_name} ({p.district or 'Hudud'})", callback_data=f"viewpost_{p.id}")])
        
    keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=t('my_posts_title', lang, count=len(posts)),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_MY_POSTS_VIEW

async def view_post_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    job_id = int(data.split('_')[1])
    job = await sync_to_async(lambda: JobPost.objects.select_related('category', 'position', 'region').filter(id=job_id).first())()
    
    if not job:
        await query.edit_message_text("E'lon topilmadi.")
        return await show_main_menu(update, context)
        
    pos_name = job.position.name_uz if job.position else (job.category.name_uz if job.category else 'Ish')
    price_str = f"{job.price_amount}" if (not job.is_price_negotiable and job.price_amount) else "Kelishilgan"
    
    gender_map = {'any': t('gender_any', lang), 'male': t('gender_male', lang), 'female': t('gender_female', lang)}
    gender_str = gender_map.get(job.gender_requirement, "Farqi yo'q")

    text = t(
        'post_detail_card',
        lang,
        id=job.id,
        title=pos_name,
        status=job.get_status_display(),
        workers_count=job.workers_count,
        gender=gender_str,
        price=price_str,
        region=job.region.name if job.region else '',
        district=job.district or '',
        start_time=job.get_start_time_type_display(),
        views_count=job.views_count,
        applications_count=job.applications_count
    )
    
    keyboard = []
    if job.applications_count > 0 or True:
        keyboard.append([InlineKeyboardButton(f"👥 Javob bergan ustalar ({job.applications_count} ta)", callback_data=f"view_post_apps_{job.id}")])

    if job.status == JobPost.Status.ACTIVE:
        keyboard.append([InlineKeyboardButton(t('btn_post_pause', lang), callback_data=f"pausepost_{job.id}")])
    elif job.status == JobPost.Status.PAUSED:
        keyboard.append([InlineKeyboardButton(t('btn_post_resume', lang), callback_data="resumepost_" + str(job.id))])
        
    keyboard.append([InlineKeyboardButton(t('btn_post_close', lang), callback_data=f"closepost_{job.id}")])
    keyboard.append([InlineKeyboardButton(t('btn_post_delete', lang), callback_data=f"delpost_{job.id}")])
    keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="menu_my_posts")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MY_POSTS_VIEW

async def post_control_action_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data.startswith("pausepost_"):
        jid = int(data.split('_')[1])
        await update_job_post_status(jid, JobPost.Status.PAUSED)
    elif data.startswith("resumepost_"):
        jid = int(data.split('_')[1])
        await update_job_post_status(jid, JobPost.Status.ACTIVE)
    elif data.startswith("closepost_"):
        jid = int(data.split('_')[1])
        await update_job_post_status(jid, JobPost.Status.COMPLETED)
    elif data.startswith("delpost_"):
        jid = int(data.split('_')[1])
        await delete_job_post(jid)
        
    return await my_posts_handler(update, context)

APP_PAGE_SIZE = 6

async def applications_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0):
    query = update.callback_query
    if query:
        await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    apps = await get_employer_applications(update.effective_user.id)
    if not apps:
        keyboard = [[InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_main_menu")]]
        msg = "📬 Hozircha sizning e'lonlaringizga nomzodlardan javoblar (отклики) tushmagan."
        if query:
            await query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.effective_message.reply_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard))
        return STATE_MAIN_MENU

    total_pages = max(1, (len(apps) + APP_PAGE_SIZE - 1) // APP_PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))
    
    start_idx = page * APP_PAGE_SIZE
    page_apps = apps[start_idx:start_idx + APP_PAGE_SIZE]

    text = f"👥 <b>KELIB TUSHGAN JAVOBLAR ({len(apps)} ta):</b>\n\nTanlash va profilini ko'rish uchun nomzodni bosing:\n<i>(Sahifa {page+1}/{total_pages})</i>"
    keyboard = []
    for a in page_apps:
        w_name = a.worker.get_full_name() or a.worker.first_name or a.worker.username or 'Nomzod'
        job_title = a.job_post.position.name_uz if a.job_post.position else (a.job_post.custom_position_name or 'Ish')
        status_icon = "⏳" if a.status == JobApplication.Status.PENDING else ("✅" if a.status == JobApplication.Status.ACCEPTED else "❌")
        btn_title = f"{status_icon} #{a.job_post_id} {w_name} ({job_title})"
        keyboard.append([InlineKeyboardButton(btn_title, callback_data=f"app_view_{a.id}")])
        
    nav_btns = []
    if page > 0:
        nav_btns.append(InlineKeyboardButton("⬅️", callback_data=f"appspage_{page-1}"))
    if total_pages > 1:
        nav_btns.append(InlineKeyboardButton(f"📄 {page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_btns.append(InlineKeyboardButton("➡️", callback_data=f"appspage_{page+1}"))
    if nav_btns:
        keyboard.append(nav_btns)
        
    keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.effective_message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU

async def show_post_applications(update: Update, context: ContextTypes.DEFAULT_TYPE, job_id: int, page: int = 0):
    query = update.callback_query
    if query:
        await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    apps = await get_employer_applications(update.effective_user.id, post_id=job_id)
    if not apps:
        keyboard = [
            [InlineKeyboardButton("⬅️ E'longa qaytish", callback_data=f"viewpost_{job_id}")],
            [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_my_posts")]
        ]
        msg = f"📬 <b>#{job_id} sonli e'longa hali nomzodlar javob yuborishmagan.</b>\n\nNomzodlar javob yuborishi bilan sizga darhol bildirishnoma yuboriladi!"
        if query:
            await query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        else:
            await update.effective_message.reply_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return STATE_MY_POSTS_VIEW

    total_pages = max(1, (len(apps) + APP_PAGE_SIZE - 1) // APP_PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))
    
    start_idx = page * APP_PAGE_SIZE
    page_apps = apps[start_idx:start_idx + APP_PAGE_SIZE]

    text = f"👥 <b>E'LON #{job_id} BO'YICHA KELGAN JAVOBLAR ({len(apps)} ta):</b>\n\nNomzod anketasi, portfoliosi va tajribasi bilan tanishish uchun tanlang:\n<i>(Sahifa {page+1}/{total_pages})</i>"
    keyboard = []
    for a in page_apps:
        w_name = a.worker.get_full_name() or a.worker.first_name or a.worker.username or 'Nomzod'
        status_icon = "⏳" if a.status == JobApplication.Status.PENDING else ("✅" if a.status == JobApplication.Status.ACCEPTED else "❌")
        btn_title = f"{status_icon} {w_name} — (Baho: {a.worker.rating}⭐️)"
        keyboard.append([InlineKeyboardButton(btn_title, callback_data=f"app_view_{a.id}")])
        
    nav_btns = []
    if page > 0:
        nav_btns.append(InlineKeyboardButton("⬅️", callback_data=f"postappspage_{job_id}_{page-1}"))
    if total_pages > 1:
        nav_btns.append(InlineKeyboardButton(f"📄 {page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_btns.append(InlineKeyboardButton("➡️", callback_data=f"postappspage_{job_id}_{page+1}"))
    if nav_btns:
        keyboard.append(nav_btns)
        
    keyboard.append([InlineKeyboardButton("⬅️ E'lon", callback_data=f"viewpost_{job_id}")])
    keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="menu_my_posts")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.effective_message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MY_POSTS_VIEW

async def show_applicant_profile(update: Update, context: ContextTypes.DEFAULT_TYPE, app_id: int):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    detail = await get_application_details_in_db(app_id)
    if not detail:
        await query.answer("Ushbu ariza topilmadi yoki o'chirilgan!", show_alert=True)
        return await show_main_menu(update, context)
        
    status_label = "⏳ Kutilmoqda (Ko'rib chiqilmoqda)" if detail['status'] == 'pending' else ("✅ Qabul qilingan" if detail['status'] == 'accepted' else "❌ Rad etilgan")
    
    # Agar qabul qilingan bo'lsa -> telefon va aloqa ko'rinadi
    contact_section = ""
    if detail['status'] == 'accepted':
        tg_link = f"@{detail['worker_tg_username']}" if detail['worker_tg_username'] else "Mavjud emas"
        contact_section = f"\n\n🔓 <b>NOMZOD ALOQA MA'LUMOTLARI:</b>\n📞 <b>Telefon:</b> {detail['worker_phone']}\n💬 <b>Telegram:</b> {tg_link}"
    else:
        contact_section = f"\n\n🔒 <i>Nomzod telefon raqami va manzili 'Ishga qabul qilish' tugmasi bosilgandan so'ng ikkala tomonga ochiladi.</i>"

    card_text = (
        f"👤 <b>NOMZOD ANKETASI & TAKLIFI</b>\n"
        f"📢 <b>E'lon:</b> #{detail['job_id']} — {detail['job_title']}\n"
        f"📊 <b>Holat:</b> {status_label}\n"
        f"🕒 <b>Yuborilgan vaqti:</b> {detail['applied_at']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Nomzod:</b> {detail['worker_name']} ({detail['worker_age']} yosh, {detail['worker_gender']})\n"
        f"📍 <b>Hudud:</b> {detail['worker_location']}\n"
        f"🛠 <b>Mutaxassisliklari:</b> {detail['worker_positions']}\n"
        f"⭐️ <b>Reyting:</b> {detail['worker_rating']} / 5.0 ({detail['worker_reviews_count']} ta sharh)\n"
        f"✅ <b>Bajarilgan ishlar:</b> {detail['worker_completed_count']} ta\n\n"
        f"💬 <b>NOMZODNING TAKLIF XABARI:</b>\n<i>\"{detail['proposal_message']}\"</i>"
        f"{contact_section}"
    )
    
    keyboard = []
    
    # Agar ish hali ochiq bo'lsa va ariza pending bo'lsa -> Ishga qabul qilish tugmasi
    if detail['job_status'] == JobPost.Status.ACTIVE and detail['status'] == 'pending':
        keyboard.append([InlineKeyboardButton("🤝 Ishga olish", callback_data=f"app_hire_{detail['id']}")])
        
    if detail.get('portfolio_photos') and len(detail['portfolio_photos']) > 0:
        keyboard.append([InlineKeyboardButton(f"🖼 Portfolio ({len(detail['portfolio_photos'])} ta)", callback_data=f"app_port_{detail['id']}")])
        
    keyboard.append([
        InlineKeyboardButton("🗑 O‘chirish", callback_data=f"app_del_{detail['id']}"),
        InlineKeyboardButton("⬅️ Orqaga qaytish", callback_data="menu_applications"),
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=card_text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MY_POSTS_VIEW

async def delete_applicant_action(update: Update, context: ContextTypes.DEFAULT_TYPE, app_id: int):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    employer_tg_id = update.effective_user.id
    
    ok = await delete_job_application_in_db(app_id, employer_tg_id)
    if ok:
        await query.answer("Nomzod arizasi muvaffaqiyatli o‘chirildi!", show_alert=True)
    else:
        await query.answer("Ariza topilmadi yoki allaqachon o‘chirilgan", show_alert=True)
        
    return await applications_menu_handler(update, context)

async def show_applicant_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE, app_id: int):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    detail = await get_application_details_in_db(app_id)
    if not detail or not detail.get('portfolio_photos'):
        await query.answer("Ushbu nomzodda portfolio rasmlari mavjud emas", show_alert=True)
        return
        
    photos = detail['portfolio_photos']
    await query.message.reply_text(f"🖼 <b>{detail['worker_name']}ning ish namunalari ({len(photos)} ta):</b>", parse_mode='HTML')
    for idx, p in enumerate(photos, 1):
        cap = f"📸 #{idx} - Ish namunasi\n" + (f"📝 {p['caption']}" if p.get('caption') else "")
        try:
            await query.message.reply_photo(photo=p['file_id'], caption=cap)
        except Exception:
            pass
            
    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data=f"app_view_{app_id}")]]
    await query.message.reply_text("<i>Namunalarni ko'rib chiqib, nomzod anketasiga qaytishingiz mumkin:</i>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MY_POSTS_VIEW

async def hire_applicant_action(update: Update, context: ContextTypes.DEFAULT_TYPE, app_id: int):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    ok, res_msg, payload = await hire_worker_for_job_in_db(app_id)
    if not ok:
        await query.answer(res_msg, show_alert=True)
        return await show_applicant_profile(update, context, app_id)
        
    # Ikkala tomonga xabarnoma yuborish
    employer_text = (
        f"🎉 <b>TABRIKLAYMIZ! SIZ NOMZODNI ISHGA QABUL QILDINGIZ!</b>\n\n"
        f"📢 <b>E'lon:</b> #{payload['job_id']} — {payload['job_title']}\n"
        f"👤 <b>Tanlangan Mutaxassis:</b> {payload['worker_name']}\n"
        f"📞 <b>Mutaxassis Telefoni:</b> {payload['worker_phone']}\n"
        f"💬 <b>Telegram:</b> @{payload['worker_username'] if payload['worker_username'] else 'Mavjud emas'}\n\n"
        f"<i>Iltimos, ishni boshlash va aniq shartlarni kelishib olish uchun mutaxassis bilan bog'laning!</i>"
    )
    
    keyboard = [
        [InlineKeyboardButton(t('btn_menu_my_posts', lang), callback_data="menu_my_posts")],
        [InlineKeyboardButton(t('btn_goto_main_menu', lang), callback_data="back_to_main_menu")]
    ]
    await query.edit_message_text(text=employer_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    
    # Mutaxassis botiga (Worker Bot) xabarnoma yuborish
    if payload.get('worker_tg_id'):
        try:
            config = await sync_to_async(BotConfig.get_config)()
            worker_bot_token = (config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')).strip()
            if worker_bot_token:
                w_bot = Bot(token=worker_bot_token)
                worker_notif = (
                    f"🎉 <b>TABRIKLAYMIZ! ISH BERUVCHI SIZNI ISHGA QABUL QILDI!</b>\n\n"
                    f"📢 <b>E'lon:</b> #{payload['job_id']} — {payload['job_title']}\n"
                    f"📍 <b>Ish manzili:</b> {payload['job_address']}\n\n"
                    f"🔓 <b>ISH BERUVCHI KONTAKTLARI:</b>\n"
                    f"👤 <b>Mijoz:</b> {payload['employer_name']}\n"
                    f"📞 <b>Telefon:</b> {payload['employer_phone']}\n"
                    f"💬 <b>Telegram:</b> @{payload['employer_username'] if payload['employer_username'] else 'Mavjud emas'}\n\n"
                    f"<i>Iltimos, zudlik bilan ish beruvchi bilan bog'lanib, ish vaqtini tasdiqlang!</i>"
                )
                w_keyboard = [
                    [InlineKeyboardButton("👥 Javobni ko'rish", callback_data=f"my_app_view_{payload['app_id']}")]
                ]
                await w_bot.send_message(
                    chat_id=payload['worker_tg_id'],
                    text=worker_notif,
                    reply_markup=InlineKeyboardMarkup(w_keyboard),
                    parse_mode='HTML'
                )
        except Exception as e:
            logger.error(f"Failed to notify worker about acceptance: {e}")
            
    return STATE_MY_POSTS_VIEW

# ==================== QO'LLAB-QUVVATLASH HANDLERS ====================

async def help_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    lang = context.user_data.get('lang', 'uz')
    support_info = await get_bot_support_info()
    
    keyboard = [
        [InlineKeyboardButton(t('btn_guide', lang), callback_data="support_guide")],
        [InlineKeyboardButton(t('btn_write_admin', lang), url="https://t.me/fullxizmat_admin")],
        [InlineKeyboardButton(t('btn_leave_feedback', lang), callback_data="support_feedback")],
        [InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = t('support_title', lang, phone=support_info['call_center_phone'])
    
    if query:
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.effective_message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU

async def show_support_guide_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    keyboard = [
        [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_help")],
        [InlineKeyboardButton(t('btn_goto_main_menu', lang), callback_data="back_to_main_menu")],
    ]
    guide_content = t('guide_text', lang)
    await query.edit_message_text(text=guide_content, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

async def support_feedback_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    keyboard = [
        [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_help")]
    ]
    await query.edit_message_text(
        text=t('prompt_feedback', lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    return STATE_SUPPORT_FEEDBACK

async def support_feedback_received_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    
    await create_client_feedback(user_id, text)
    await update.message.reply_text(t('feedback_received', lang), parse_mode='HTML')
    return await show_main_menu(update, context)

async def profile_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    name = context.user_data.get('name') or update.effective_user.first_name
    phone = context.user_data.get('phone') or 'Kiritilgan'
    
    text = (
        f"👤 <b>ISH BERUVCHI PROFILI:</b>\n\n"
        f"👤 <b>F.I.Sh:</b> {name}\n"
        f"📞 <b>Telefon:</b> {phone}\n"
        f"🌐 <b>Tanlangan til:</b> {lang.upper()}\n"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 Ma'lumotlarni qayta kiritish", callback_data="reauth_profile")],
        [InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU
# ==================== SOZLAMALAR (SETTINGS) HANDLERS ====================

async def settings_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    keyboard = [
        [InlineKeyboardButton(t('btn_settings_lang', lang), callback_data="settings_lang")],
        [InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = t('settings_title', lang)
    if query:
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.effective_message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU

async def settings_lang_choice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'uz')
    
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O‘zbekcha (Lotin)", callback_data="setlang_uz"),
            InlineKeyboardButton("🇺🇿 Ўзбекча (Крилл)", callback_data="setlang_oz"),
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en"),
        ],
        [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=t('choose_new_lang', lang),
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_MAIN_MENU

async def set_lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    new_lang = query.data.replace('setlang_', '')
    context.user_data['lang'] = new_lang
    
    # DB da foydalanuvchi tilini yangilash
    user_id = update.effective_user.id
    await sync_to_async(lambda: User.objects.filter(telegram_id=user_id).update(language=new_lang))()
    
    await query.answer(t('lang_updated_success', new_lang).replace('<b>', '').replace('</b>', ''), show_alert=True)
    return await show_main_menu(update, context)

# ==================== FALLBACK & UNHANDLED ====================

async def unhandled_callback_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    
    lang = context.user_data.get('lang', 'uz')
    if update.effective_user:
        client = await get_client_user(update.effective_user.id)
        if client and client.get('language'):
            lang = client['language']
            
    keyboard = [
        [InlineKeyboardButton(t('btn_goto_main_menu', lang), callback_data="reset_to_main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            text=t('bot_outdated_button_msg', lang),
            reply_markup=None,
            parse_mode='HTML'
        )
    except Exception:
        await query.message.reply_text(
            text=t('bot_outdated_button_msg', lang),
            reply_markup=None,
            parse_mode='HTML'
        )

async def reset_to_main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha eski sessiyani tozalab to'g'ridan to'g'ri bosh menyuni ochib beradi"""
    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.message.delete()
        except Exception:
            pass
    context.user_data.clear()
    return await start_command(update, context)

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception in client bot while handling update: {context.error}", exc_info=context.error)
    try:
        lang = 'uz'
        if context.user_data and 'lang' in context.user_data:
            lang = context.user_data['lang']
        elif isinstance(update, Update) and update.effective_user:
            client = await get_client_user(update.effective_user.id)
            if client and client.get('language'):
                lang = client['language']
            
        error_msg = t('bot_error_msg', lang)
        if isinstance(update, Update):
            if update.callback_query:
                try:
                    await update.callback_query.answer()
                except Exception:
                    pass
                if update.callback_query.message:
                    try:
                        await update.callback_query.message.reply_text(error_msg, reply_markup=None, parse_mode='HTML')
                    except Exception:
                        pass
            elif update.effective_message:
                try:
                    await update.effective_message.reply_text(error_msg, reply_markup=None, parse_mode='HTML')
                except Exception:
                    pass
    except Exception as e:
        logger.error(f"Failed to send error message to client user: {e}")

async def post_manual_region_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi viloyatni qo'lda tanlashni bosganda barcha viloyatlar ro'yxatini 2 ustunda chiqaradi"""
    lang = context.user_data.get('lang', 'uz')
    regions = await get_all_regions()
    keyboard = []
    row = []
    for r in regions:
        r_name = r.get(f'name_{lang}') or r.get('name_uz') or 'Viloyat'
        row.append(InlineKeyboardButton(r_name, callback_data=f"reg_{r['id']}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_price")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg_text = "🏛 <b>Viloyat / Shaharni tanlang:</b>"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=msg_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(text=msg_text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_POST_MANUAL_REGION

# ==================== APPLICATION BUILDER ====================

def build_client_bot_application(token: str) -> Application:
    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_command),
            CommandHandler('menu', show_main_menu),
            CallbackQueryHandler(start_command, pattern='^start_again$'),
            CallbackQueryHandler(reset_to_main_menu_callback, pattern='^reset_to_main_menu$'),
        ],
        states={
            STATE_AUTH_LANG: [
                CallbackQueryHandler(auth_lang_handler, pattern='^lang_'),
                CallbackQueryHandler(show_main_menu, pattern='^back_to_main_menu$'),
            ],
            STATE_AUTH_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, auth_name_handler),
                CallbackQueryHandler(start_command, pattern='^start_again$'),
            ],
            STATE_AUTH_PHONE: [
                MessageHandler(filters.CONTACT, auth_phone_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, auth_phone_handler),
                CallbackQueryHandler(start_command, pattern='^start_again$'),
            ],
            STATE_MAIN_MENU: [
                CallbackQueryHandler(start_job_post_flow, pattern='^menu_new_post$'),
                CallbackQueryHandler(my_posts_handler, pattern='^menu_my_posts$'),
                CallbackQueryHandler(applications_menu_handler, pattern='^menu_applications$'),
                CallbackQueryHandler(lambda u, c: applications_menu_handler(u, c, int(u.callback_query.data.replace('appspage_', ''))), pattern='^appspage_'),
                CallbackQueryHandler(lambda u, c: show_applicant_profile(u, c, int(u.callback_query.data.replace('app_view_', ''))), pattern='^app_view_'),
                CallbackQueryHandler(profile_menu_handler, pattern='^menu_profile$'),
                CallbackQueryHandler(settings_menu_handler, pattern='^menu_settings$'),
                CallbackQueryHandler(settings_lang_choice_handler, pattern='^settings_lang$'),
                CallbackQueryHandler(set_lang_handler, pattern='^setlang_'),
                CallbackQueryHandler(help_menu_handler, pattern='^menu_help$'),
                CallbackQueryHandler(show_support_guide_handler, pattern='^support_guide$'),
                CallbackQueryHandler(support_feedback_start_handler, pattern='^support_feedback$'),
                CallbackQueryHandler(start_command, pattern='^reauth_profile$'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_EMP_TYPE: [
                CallbackQueryHandler(post_emp_type_handler, pattern='^emp_type_'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_CATEGORY: [
                CallbackQueryHandler(post_category_handler, pattern='^(cat_|catpage_|back_to_emp_type)'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_POSITION: [
                CallbackQueryHandler(post_position_handler, pattern='^(pos_|pospage_|back_to_categories)'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, post_description_handler),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_PHOTO: [
                CallbackQueryHandler(post_photo_handler, pattern='^skip_photo$'),
                MessageHandler(filters.PHOTO, post_photo_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, post_photo_handler),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_WORKERS_COUNT: [
                CallbackQueryHandler(post_workers_count_handler, pattern='^wc_'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_GENDER: [
                CallbackQueryHandler(post_gender_handler, pattern='^g_'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_START_TIME: [
                CallbackQueryHandler(post_start_time_handler, pattern='^st_'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_CUSTOM_START: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, post_custom_start_handler),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_PRICE_TYPE: [
                CallbackQueryHandler(post_price_type_handler, pattern='^pr_'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_PRICE_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, post_price_amount_handler),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_LOCATION: [
                MessageHandler(filters.LOCATION, post_location_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, post_location_handler),
                CallbackQueryHandler(post_manual_region_start_handler, pattern='^reg_manual$'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_MANUAL_REGION: [
                CallbackQueryHandler(post_manual_region_handler, pattern='^reg_'),
                CallbackQueryHandler(ask_price_step, pattern='^back_to_price$'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_MANUAL_DISTRICT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, post_manual_district_handler),
                CallbackQueryHandler(post_manual_region_start_handler, pattern='^back_to_regions$'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, post_address_handler),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_REVIEW: [
                CallbackQueryHandler(post_review_action_handler, pattern='^(confirm_job_post|change_post_contact|cancel_job_post)'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_POST_CHANGE_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, post_change_phone_handler),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_MY_POSTS_VIEW: [
                CallbackQueryHandler(view_post_detail_handler, pattern='^viewpost_'),
                CallbackQueryHandler(post_control_action_handler, pattern='^(pausepost_|resumepost_|closepost_|delpost_)'),
                CallbackQueryHandler(lambda u, c: show_post_applications(u, c, int(u.callback_query.data.replace('view_post_apps_', ''))), pattern='^view_post_apps_'),
                CallbackQueryHandler(lambda u, c: show_post_applications(u, c, int(u.callback_query.data.split('_')[1]), int(u.callback_query.data.split('_')[2])), pattern='^postappspage_'),
                CallbackQueryHandler(lambda u, c: applications_menu_handler(u, c, int(u.callback_query.data.replace('appspage_', ''))), pattern='^appspage_'),
                CallbackQueryHandler(lambda u, c: show_applicant_profile(u, c, int(u.callback_query.data.replace('app_view_', ''))), pattern='^app_view_'),
                CallbackQueryHandler(lambda u, c: show_applicant_portfolio(u, c, int(u.callback_query.data.replace('app_port_', ''))), pattern='^app_port_'),
                CallbackQueryHandler(lambda u, c: hire_applicant_action(u, c, int(u.callback_query.data.replace('app_hire_', ''))), pattern='^app_hire_'),
                CallbackQueryHandler(lambda u, c: delete_applicant_action(u, c, int(u.callback_query.data.replace('app_del_', ''))), pattern='^app_del_'),
                CallbackQueryHandler(show_support_guide_handler, pattern='^support_guide$'),
                CallbackQueryHandler(support_feedback_start_handler, pattern='^support_feedback$'),
                CallbackQueryHandler(help_menu_handler, pattern='^menu_help$'),
                CallbackQueryHandler(my_posts_handler, pattern='^menu_my_posts$'),
                CallbackQueryHandler(applications_menu_handler, pattern='^menu_applications$'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
            STATE_SUPPORT_FEEDBACK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, support_feedback_received_handler),
                CallbackQueryHandler(help_menu_handler, pattern='^menu_help$'),
                CallbackQueryHandler(show_main_menu, pattern='^(back_to_main_menu|reset_to_main_menu)$'),
            ],
        },
        fallbacks=[
            CommandHandler('start', start_command),
            CommandHandler('menu', show_main_menu),
            CallbackQueryHandler(lambda u, c: show_post_applications(u, c, int(u.callback_query.data.replace('view_post_apps_', ''))), pattern='^view_post_apps_'),
            CallbackQueryHandler(lambda u, c: show_post_applications(u, c, int(u.callback_query.data.split('_')[1]), int(u.callback_query.data.split('_')[2])), pattern='^postappspage_'),
            CallbackQueryHandler(lambda u, c: applications_menu_handler(u, c, int(u.callback_query.data.replace('appspage_', ''))), pattern='^appspage_'),
            CallbackQueryHandler(lambda u, c: show_applicant_profile(u, c, int(u.callback_query.data.replace('app_view_', ''))), pattern='^app_view_'),
            CallbackQueryHandler(lambda u, c: show_applicant_portfolio(u, c, int(u.callback_query.data.replace('app_port_', ''))), pattern='^app_port_'),
            CallbackQueryHandler(lambda u, c: hire_applicant_action(u, c, int(u.callback_query.data.replace('app_hire_', ''))), pattern='^app_hire_'),
            CallbackQueryHandler(lambda u, c: delete_applicant_action(u, c, int(u.callback_query.data.replace('app_del_', ''))), pattern='^app_del_'),
            CallbackQueryHandler(show_support_guide_handler, pattern='^support_guide$'),
            CallbackQueryHandler(support_feedback_start_handler, pattern='^support_feedback$'),
            CallbackQueryHandler(settings_menu_handler, pattern='^menu_settings$'),
            CallbackQueryHandler(settings_lang_choice_handler, pattern='^settings_lang$'),
            CallbackQueryHandler(set_lang_handler, pattern='^setlang_'),
            CallbackQueryHandler(help_menu_handler, pattern='^menu_help$'),
            CallbackQueryHandler(reset_to_main_menu_callback, pattern='^reset_to_main_menu$'),
            CallbackQueryHandler(show_main_menu, pattern='^back_to_main_menu$'),
            CallbackQueryHandler(unhandled_callback_fallback, pattern='.*'),
        ],
        allow_reentry=True
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(reset_to_main_menu_callback, pattern='^reset_to_main_menu$'))
    app.add_handler(CallbackQueryHandler(show_main_menu, pattern='^back_to_main_menu$'))
    app.add_handler(CallbackQueryHandler(unhandled_callback_fallback, pattern='.*'))
    app.add_error_handler(global_error_handler)

    return app
