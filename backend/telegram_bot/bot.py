# -*- coding: utf-8 -*-
import os
import sys
import logging
import math
import re

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
from django.db.models import Q
from accounts.models import User, WorkerPortfolio, WorkerReview, UserFeedback
from categories.models import Category, Position
from locations.models import Region, reverse_geocode
from orders.models import Order, JobPost, JobApplication
from bot_control.models import BotConfig

from .texts import t, TEXTS

from telegram import (
    Update,
    Bot,
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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# STATES (0-QADAMDAN 5-QADAMGANI VA MENYU HOLATLARI)
(
    STATE_LANGUAGE,              # 0-QADAM: Til tanlash
    STATE_ROLE,                  # 0.1-QADAM: Rol tanlash
    STATE_GENDER,                # 1.1: Jinsni tanlash
    STATE_FULL_NAME,             # 1.2: Ism-familiya
    STATE_AGE,                   # 1.3: Yosh
    STATE_PHONE,                 # 1.4: Telefon raqam
    STATE_GEO_LOCATION,          # 2.1: GPS Lokatsiya
    STATE_MANUAL_REGION,         # 2.1-alt: Viloyat tanlash
    STATE_STREET_ADDRESS,        # 2.2: Mahalla / ko'cha / uy
    STATE_CATEGORY,              # 3.1: Asosiy soha
    STATE_CUSTOM_CATEGORY,       # 3.1-alt: Qo'lda soha
    STATE_POSITION,              # 3.2: Mutaxassisliklar (Multi-select 10 tagacha)
    STATE_CUSTOM_POSITION,       # 3.2-alt: Qo'lda mutaxassislik
    STATE_EMPLOYMENT_TYPE,       # 4.1: Bandlik turi
    STATE_WORK_SCHEDULE,         # 4.2: Ish vaqti
    STATE_CONFIRM_PROFILE,       # 5: Anketani tasdiqlash
    STATE_MAIN_MENU,             # Asosiy menyu
    STATE_UPDATE_LOCATION,       # Menyudan lokatsiyani yangilash
    STATE_PORTFOLIO_ADD_PHOTO,   # Portfolio yangi namuna: Rasm kutish
    STATE_PORTFOLIO_ADD_CAPTION, # Portfolio yangi namuna: Izoh kutish
    STATE_PORTFOLIO_EDIT_CAPTION,# Portfolio: Izohni tahrirlash
    STATE_PORTFOLIO_REPLACE_PHOTO,# Portfolio: Rasmni almashtirish
    STATE_SEND_FEEDBACK,         # Taklif / shikoyat yuborish
    STATE_EDIT_NAME_AGE,         # Tahrirlash: Ism va yosh
    STATE_EDIT_PHONE,            # Tahrirlash: Telefon
    STATE_APPLY_PROPOSAL_MSG,    # Ishga so'rov: Xabar matnini kiritish
    STATE_APPLY_PROPOSAL_CONFIRM,# Ishga so'rov: Yuborishni tasdiqlash
) = range(27)

PAGE_SIZE = 8

# ==================== DB ASYNC FUNKSIYALARI ====================

@sync_to_async
def get_user_db_record(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None

    # Majburiy maydonlar to'ldirilganligini qat'iy tekshirish
    has_positions = user.selected_positions.exists() or bool(user.position_id) or bool(user.custom_position)
    has_location = bool(user.region_id or (user.latitude and user.longitude))
    is_fully_complete = bool(
        user.is_registered and 
        user.phone_number and 
        user.first_name and 
        user.gender and 
        user.age and 
        has_location and 
        has_positions and 
        not user.needs_profile_update
    )
    has_existing_profile = bool(user.is_registered and user.phone_number and user.first_name)

    return {
        'id': user.id,
        'telegram_id': user.telegram_id,
        'first_name': user.first_name,
        'language': user.language or 'uz',
        'is_registered': is_fully_complete,
        'has_existing_profile': has_existing_profile,
        'is_busy': user.is_busy,
        'role': user.role,
        'needs_profile_update': user.needs_profile_update,
        'profile_update_reason': user.profile_update_reason or '',
        'profile_update_fields': user.profile_update_fields or '',
    }

@sync_to_async
def record_lead_worker(telegram_id: int, username: str = '', first_name: str = '', last_name: str = '', lang: str = 'uz'):
    """
    Botga /start bosgan yoki kirgan foydalanuvchini lid sifatida DBda saqlash yoki yangilash.
    Agar ro'yxatdan to'liq o'tgan bo'lsa, uning ro'yxatdan o'tgan holatini buzmaydi.
    """
    user, created = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'username': username or f"tg_{telegram_id}",
            'first_name': first_name or '',
            'last_name': last_name or '',
            'role': User.Role.WORKER,
            'language': lang or 'uz',
            'is_registered': False,
            'started_worker_bot': True,
        }
    )
    # Agar mavjud bo'lsa, username/first_name/started_worker_bot ni yangilab qo'yamiz
    update_fields = []
    if not user.started_worker_bot:
        user.started_worker_bot = True
        update_fields.append('started_worker_bot')
    if username and user.username != username:
        user.username = username
        update_fields.append('username')
    if first_name and not user.first_name:
        user.first_name = first_name
        update_fields.append('first_name')
    if last_name and not user.last_name:
        user.last_name = last_name
        update_fields.append('last_name')
    if lang and not user.language:
        user.language = lang
        update_fields.append('language')
    if update_fields:
        user.save(update_fields=update_fields)
    return user

@sync_to_async
def get_all_registered_users_for_notification():
    return list(User.objects.filter(is_registered=True, telegram_id__isnull=False).values('telegram_id', 'language', 'first_name'))

@sync_to_async
def save_full_profile_to_db(telegram_id: int, username: str, data: dict):
    user, _ = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'username': username or f"tg_{telegram_id}",
            'role': User.Role.WORKER,
        }
    )
    user.language = data.get('lang', 'uz')
    user.role = User.Role.WORKER
    user.gender = data.get('gender', 'male')
    user.first_name = data.get('full_name', user.first_name or username or '')
    user.age = data.get('age', 25)
    user.phone_number = data.get('phone', '')
    
    if data.get('region_id'):
        user.region_id = data['region_id']
    user.district = data.get('district', '')
    user.street_address = data.get('street_address', '')
    user.latitude = data.get('latitude')
    user.longitude = data.get('longitude')
    
    if data.get('category_id'):
        user.category_id = data['category_id']
    user.custom_category = data.get('custom_category')
    user.custom_position = data.get('custom_position')
    
    user.employment_type = data.get('employment_type', User.EmploymentType.BOTH)
    user.work_schedule = data.get('work_schedule', User.WorkSchedule.FLEXIBLE)
    user.is_registered = True
    user.needs_profile_update = False
    user.profile_update_reason = ''
    user.profile_update_fields = ''
    user.is_busy = False
    user.started_worker_bot = True
    user.save()
    
    pos_ids = list(data.get('selected_pos_ids', []))
    if pos_ids:
        user.position_id = pos_ids[0]
        user.selected_positions.set(pos_ids)
    elif data.get('position_id'):
        user.position_id = data['position_id']
        user.selected_positions.set([data['position_id']])
        
    user.save()
    return user

@sync_to_async
def get_user_profile(telegram_id: int):
    try:
        user = User.objects.select_related('region', 'category', 'position').prefetch_related('selected_positions').get(telegram_id=telegram_id)
        positions = list(user.selected_positions.all())
        lang = user.language or 'uz'
        
        if positions:
            pos_names = [p.get_name(lang) for p in positions]
            pos_str = ", ".join(pos_names)
            pos_count = len(positions)
        elif user.position:
            pos_str = user.position.get_name(lang)
            pos_count = 1
        elif user.custom_position:
            pos_str = user.custom_position
            pos_count = 1
        else:
            pos_str = "Tanlanmagan"
            pos_count = 0
            
        gps_str = f"{user.latitude:.5f}, {user.longitude:.5f}" if (user.latitude and user.longitude) else "Kiritilmagan"
        has_location = bool(user.region or (user.latitude and user.longitude))
        
        emp_type_map = {
            'daily': t('emp_type_daily', lang),
            'permanent': t('emp_type_permanent', lang),
            'both': t('emp_type_both', lang),
        }
        schedule_map = {
            'day_shift': t('schedule_day', lang),
            '24_7': t('schedule_24_7', lang),
            'flexible': t('schedule_flexible', lang),
        }
        gender_map = {
            'male': t('gender_male', lang),
            'female': t('gender_female', lang),
        }
        
        reviews_count = user.received_reviews.count()
        portfolios_count = user.portfolio_items.count()

        return {
            'name': user.first_name or user.username,
            'gender': gender_map.get(user.gender, t('gender_male', lang)),
            'age': user.age or 25,
            'phone': user.phone_number or 'Mavjud emas',
            'user_lang': user.get_language_display(),
            'lang_code': user.language or 'uz',
            'role': user.role,
            'is_busy': user.is_busy,
            'is_registered': user.is_registered,
            'region': user.region.get_name(lang) if user.region else 'Tanlanmagan',
            'region_id': user.region_id,
            'district': user.district or '',
            'street_address': user.street_address or '',
            'category': user.category.get_name(lang) if user.category else (user.custom_category or 'Tanlanmagan'),
            'category_id': user.category_id,
            'positions': pos_str,
            'pos_count': pos_count,
            'emp_type': emp_type_map.get(user.employment_type, t('emp_type_both', lang)),
            'work_schedule': schedule_map.get(user.work_schedule, t('schedule_flexible', lang)),
            'rating': user.rating,
            'completed_count': user.completed_jobs_count,
            'reviews_count': reviews_count,
            'portfolios_count': portfolios_count,
            'notification_setting': user.notification_setting,
            'latitude': user.latitude,
            'longitude': user.longitude,
            'gps': gps_str,
            'has_location': has_location,
        }
    except Exception as e:
        logger.error(f"Error fetching profile: {e}")
        return None

@sync_to_async
def toggle_user_busy_status(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if user:
        user.is_busy = not user.is_busy
        user.save(update_fields=['is_busy'])
        return user.is_busy
    return False

@sync_to_async
def set_user_busy_status(telegram_id: int, is_busy: bool):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if user:
        user.is_busy = is_busy
        user.save(update_fields=['is_busy'])
        return user.is_busy
    return is_busy

@sync_to_async
def update_user_language(telegram_id: int, lang: str):
    User.objects.filter(telegram_id=telegram_id).update(language=lang)

@sync_to_async
def update_user_notification(telegram_id: int, mode: str):
    User.objects.filter(telegram_id=telegram_id).update(notification_setting=mode)

@sync_to_async
def save_user_portfolio_item(telegram_id: int, file_id: str, caption: str = ""):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return False, "User topilmadi"
    if user.portfolio_items.count() >= 5:
        return False, "LIMIT"
    item = WorkerPortfolio.objects.create(worker=user, file_id=file_id, caption=caption)
    return True, user.portfolio_items.count()

@sync_to_async
def get_user_portfolio_photos(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return []
    return list(user.portfolio_items.all().order_by('created_at').values('id', 'file_id', 'caption', 'created_at'))

@sync_to_async
def update_portfolio_caption(photo_id: int, telegram_id: int, caption: str):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if user:
        WorkerPortfolio.objects.filter(id=photo_id, worker=user).update(caption=caption)
        return True
    return False

@sync_to_async
def replace_portfolio_photo(photo_id: int, telegram_id: int, file_id: str):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if user:
        WorkerPortfolio.objects.filter(id=photo_id, worker=user).update(file_id=file_id)
        return True
    return False

@sync_to_async
def delete_user_portfolio_photo(photo_id: int, telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if user:
        WorkerPortfolio.objects.filter(id=photo_id, worker=user).delete()
        return True
    return False

@sync_to_async
def get_user_reviews(telegram_id: int, page: int = 1, page_size: int = 3):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return [], 1, 1, 5.0, 0
    
    qs = WorkerReview.objects.filter(worker=user).order_by('-created_at')
    total_count = qs.count()
    total_pages = max(1, math.ceil(total_count / page_size))
    page = max(1, min(page, total_pages))
    
    start = (page - 1) * page_size
    items = list(qs[start:start + page_size])
    reviews_data = [
        {
            'client_name': r.client_name,
            'rating': r.rating,
            'comment': r.comment,
            'date': r.created_at.strftime("%d.%m.%Y"),
        } for r in items
    ]
    return reviews_data, page, total_pages, user.rating, user.completed_jobs_count

@sync_to_async
def create_user_feedback(telegram_id: int, text: str):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if user:
        UserFeedback.objects.create(user=user, message=text)
        return True
    return False

@sync_to_async
def save_location_from_gps(telegram_id: int, lat: float, lon: float):
    geo_res = reverse_geocode(lat, lon)
    region_id = geo_res.get('region_id')
    region_obj = None
    if region_id:
        region_obj = Region.objects.filter(id=region_id).first()
    if not region_obj and geo_res.get('region_name'):
        reg_search = geo_res['region_name'].lower()
        region_obj = Region.objects.filter(name_uz__icontains=reg_search).first()
        if not region_obj:
            for r in Region.objects.all():
                if any(kw in r.name_uz.lower() for kw in reg_search.split()):
                    region_obj = r
                    break
    
    district = geo_res.get('district', '') or geo_res.get('road', '')
    if telegram_id:
        user = User.objects.filter(telegram_id=telegram_id).first()
        if user:
            user.latitude = lat
            user.longitude = lon
            user.district = district
            if region_obj:
                user.region = region_obj
            user.save(update_fields=['latitude', 'longitude', 'district', 'region'] if region_obj else ['latitude', 'longitude', 'district'])
            
            # Shuningdek WorkerLocation modelini ham yangilaymiz
            from locations.models import WorkerLocation
            WorkerLocation.objects.update_or_create(
                worker=user,
                defaults={'latitude': lat, 'longitude': lon}
            )
        
    return {
        'region_id': region_obj.id if region_obj else None,
        'region_name': region_obj.name_uz if region_obj else (geo_res.get('region_name') or "O'zbekiston"),
        'district': district,
    }

@sync_to_async
def get_active_regions(lang: str = 'uz'):
    regions = list(Region.objects.filter(is_active=True).order_by('order', 'id'))
    return [(r.id, r.get_name(lang)) for r in regions]

@sync_to_async
def get_categories_page(lang: str = 'uz', page: int = 1, page_size: int = PAGE_SIZE):
    qs = Category.objects.filter(is_active=True).order_by('order', 'id')
    total_count = qs.count()
    total_pages = max(1, math.ceil(total_count / page_size))
    page = max(1, min(page, total_pages))
    
    start = (page - 1) * page_size
    items = list(qs[start:start + page_size])
    return [(c.id, f"{c.icon} {c.get_name(lang)}") for c in items], page, total_pages

@sync_to_async
def get_positions_page(category_id: int, lang: str = 'uz', page: int = 1, page_size: int = PAGE_SIZE):
    qs = Position.objects.filter(category_id=category_id, is_active=True).order_by('order', 'id')
    total_count = qs.count()
    total_pages = max(1, math.ceil(total_count / page_size))
    page = max(1, min(page, total_pages))
    
    start = (page - 1) * page_size
    items = list(qs[start:start + page_size])
    return [(p.id, p.get_name(lang)) for p in items], page, total_pages

def calculate_distance_km(lat1, lon1, lat2, lon2):
    try:
        if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
            return 99999.0
        f_lat1 = float(lat1)
        f_lon1 = float(lon1)
        f_lat2 = float(lat2)
        f_lon2 = float(lon2)
        
        r = 6371.0
        dlat = math.radians(f_lat2 - f_lat1)
        dlon = math.radians(f_lon2 - f_lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(f_lat1)) * math.cos(math.radians(f_lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c
    except Exception:
        return 99999.0

@sync_to_async
def fetch_jobs_feed(telegram_id: int, filter_type: str = 'matched', cat_id: int = None, radius: int = None):
    user = User.objects.filter(telegram_id=telegram_id).first()
    lang = user.language if user and user.language else 'uz'
    
    # Query active JobPosts
    job_qs = JobPost.objects.filter(status=JobPost.Status.ACTIVE).select_related('category', 'position', 'region', 'employer')
    # Query pending Orders
    order_qs = Order.objects.filter(status=Order.Status.PENDING).select_related('category')
    
    if filter_type in ['matched', 'all']:
        # "Barcha ishlar" - barcha faol e'lonlar va buyurtmalar ko'rsatiladi
        pass
    elif filter_type == 'category' and cat_id:
        job_qs = job_qs.filter(category_id=cat_id)
        order_qs = order_qs.filter(category_id=cat_id)
    elif filter_type == 'district' and user and user.district:
        job_qs = job_qs.filter(Q(district__icontains=user.district) | Q(address__icontains=user.district))
        order_qs = order_qs.filter(address__icontains=user.district)
    elif filter_type == 'region' and user and user.region:
        job_qs = job_qs.filter(Q(region_id=user.region_id) | Q(address__icontains=user.region.name_uz))
        order_qs = order_qs.filter(address__icontains=user.region.name_uz)

    # Convert JobPosts
    results = []
    for job in job_qs.order_by('-created_at')[:50]:
        # Handle radius filtering if requested
        distance_str = ""
        if filter_type == 'radius' and radius:
            if user and user.latitude and user.longitude and job.latitude and job.longitude:
                dist = calculate_distance_km(user.latitude, user.longitude, job.latitude, job.longitude)
                if dist > radius:
                    continue
                distance_str = f" (~{dist:.1f} km)"
            elif user and user.district and job.district:
                if user.district.lower() not in job.district.lower() and job.district.lower() not in user.district.lower():
                    continue
            elif user and user.region and job.region:
                if user.region_id != job.region_id:
                    continue

        pos_name = job.position.get_name(lang) if job.position else (job.custom_position_name or 'Mutaxassis')
        cat_name = job.category.get_name(lang) if job.category else 'Boshqa'
        
        # Format start time
        if job.start_time_type == JobPost.StartTimeType.URGENT:
            time_display = "🔥 Tezkor (Bugun)"
        elif job.start_time_type == JobPost.StartTimeType.TOMORROW:
            time_display = "🗓 Ertaga"
        else:
            time_display = job.custom_start_date or "Kelishilgan vaqtda"
            
        # Price display
        if job.is_price_negotiable and not job.price_amount:
            price_display = "🤝 Narxi kelishiladi"
        elif job.price_amount:
            price_display = f"💰 {job.price_amount}"
        else:
            price_display = "🤝 Kelishiladi"
            
        # Location display
        loc_parts = []
        if job.region:
            loc_parts.append(job.region.get_name(lang))
        if job.district:
            loc_parts.append(job.district)
        if job.address:
            loc_parts.append(job.address)
        loc_display = ", ".join(loc_parts) if loc_parts else "Ko'rsatilmagan"
        if distance_str:
            loc_display += distance_str
            
        results.append({
            'id': f"JP-{job.id}",
            'raw_id': job.id,
            'type': 'job_post',
            'title': pos_name,
            'category': cat_name,
            'service_type': pos_name,
            'address': loc_display,
            'work_time': time_display,
            'work_format': job.get_employment_type_display(),
            'desc': job.description or "Batafsil ma'lumot berilmagan",
            'price': price_display,
            'customer_name': job.contact_name or (job.employer.get_full_name() if job.employer else 'Ish beruvchi'),
            'contact': job.contact_phone or (job.employer.phone_number if job.employer else '+998 (71) 200-00-00'),
            'contact_tg': job.contact_telegram_username or '',
            'photo_file_id': job.photo_file_id,
            'workers_count': job.workers_count,
            'gender': job.get_gender_requirement_display(),
            'date': job.created_at.strftime("%d.%m.%Y %H:%M") if job.created_at else "",
            'timestamp': job.created_at.timestamp() if job.created_at else 0
        })

    # Convert Orders
    if filter_type != 'radius':
        for ord in order_qs.order_by('-created_at')[:20]:
            cat_name = ord.category.get_name(lang) if ord.category else 'Boshqa'
            price_disp = f"💰 {ord.price:,.0f} so'm" if ord.price else "🤝 Kelishiladi"
            results.append({
                'id': f"ORD-{ord.id}",
                'raw_id': ord.id,
                'type': 'order',
                'title': ord.title or 'Ish xizmati',
                'category': cat_name,
                'service_type': ord.service_type or 'Usta xizmati',
                'address': ord.address or "Ko'rsatilmagan",
                'work_time': 'Bugun / Tezkor',
                'work_format': ord.get_work_format_display(),
                'desc': ord.description or "Batafsil ma'lumot keltirilmagan",
                'price': price_disp,
                'customer_name': ord.customer_name or 'Mijoz',
                'contact': ord.customer_phone or '+998 (71) 200-00-00',
                'contact_tg': '',
                'photo_file_id': None,
                'workers_count': '1 nafar',
                'gender': 'Farqi yo\'q',
                'date': ord.created_at.strftime("%d.%m.%Y %H:%M") if ord.created_at else "",
                'timestamp': ord.created_at.timestamp() if ord.created_at else 0
            })

    # Sort combined by most recent timestamp
    results.sort(key=lambda x: x['timestamp'], reverse=True)
    return results

@sync_to_async
def fetch_single_job_post(job_id: int, lang: str = 'uz'):
    job = JobPost.objects.select_related('employer', 'position', 'category', 'region').filter(id=job_id).first()
    if not job:
        return None
    pos_name = job.position.get_name(lang) if job.position else (job.custom_position_name or 'Mutaxassis')
    cat_name = job.category.get_name(lang) if job.category else 'Boshqa'
    
    if job.start_time_type == JobPost.StartTimeType.URGENT:
        time_display = "🔥 Tezkor (Bugun)"
    elif job.start_time_type == JobPost.StartTimeType.TOMORROW:
        time_display = "🗓 Ertaga"
    else:
        time_display = job.custom_start_date or "Kelishilgan vaqtda"
        
    if job.is_price_negotiable and not job.price_amount:
        price_display = "🤝 Narxi kelishiladi"
    elif job.price_amount:
        price_display = f"💰 {job.price_amount}"
    else:
        price_display = "🤝 Kelishiladi"
        
    loc_parts = []
    if job.region:
        loc_parts.append(job.region.get_name(lang))
    if job.district:
        loc_parts.append(job.district)
    if job.address:
        loc_parts.append(job.address)
    loc_display = ", ".join(loc_parts) if loc_parts else "Ko'rsatilmagan"
    
    return {
        'id': f"JP-{job.id}",
        'raw_id': job.id,
        'type': 'job_post',
        'title': pos_name,
        'category': cat_name,
        'service_type': pos_name,
        'address': loc_display,
        'work_time': time_display,
        'work_format': job.get_employment_type_display(),
        'desc': job.description or "Batafsil ma'lumot berilmagan",
        'price': price_display,
        'customer_name': job.contact_name or (job.employer.get_full_name() if job.employer else 'Ish beruvchi'),
        'contact': job.contact_phone or (job.employer.phone_number if job.employer else '+998 (71) 200-00-00'),
        'contact_tg': job.contact_telegram_username or '',
        'photo_file_id': job.photo_file_id,
        'workers_count': job.workers_count,
        'gender': job.get_gender_requirement_display(),
        'date': job.created_at.strftime("%d.%m.%Y %H:%M") if job.created_at else "",
        'timestamp': job.created_at.timestamp() if job.created_at else 0
    }

@sync_to_async
def fetch_single_order(order_id: int, lang: str = 'uz'):
    ord = Order.objects.select_related('category').filter(id=order_id).first()
    if not ord:
        return None
    cat_name = ord.category.get_name(lang) if ord.category else 'Boshqa'
    price_disp = f"💰 {ord.price:,.0f} so'm" if ord.price else "🤝 Kelishiladi"
    return {
        'id': f"ORD-{ord.id}",
        'raw_id': ord.id,
        'type': 'order',
        'title': ord.title or 'Ish xizmati',
        'category': cat_name,
        'service_type': ord.service_type or 'Usta xizmati',
        'address': ord.address or "Ko'rsatilmagan",
        'work_time': 'Bugun / Tezkor',
        'work_format': ord.get_work_format_display(),
        'desc': ord.description or "Batafsil ma'lumot keltirilmagan",
        'price': price_disp,
        'customer_name': ord.customer_name or 'Mijoz',
        'contact': ord.customer_phone or '+998 (71) 200-00-00',
        'contact_tg': '',
        'photo_file_id': None,
        'workers_count': '1 nafar',
        'gender': 'Farqi yo\'q',
        'date': ord.created_at.strftime("%d.%m.%Y %H:%M") if ord.created_at else "",
        'timestamp': ord.created_at.timestamp() if ord.created_at else 0
    }

async def fetch_single_job(identifier: str or int, lang: str = 'uz'):
    id_str = str(identifier).strip()
    if id_str.startswith("JP-"):
        raw_id = int(id_str.replace("JP-", ""))
        return await fetch_single_job_post(raw_id, lang)
    elif id_str.startswith("ORD-"):
        raw_id = int(id_str.replace("ORD-", ""))
        return await fetch_single_order(raw_id, lang)
    else:
        try:
            raw_id = int(id_str)
            job = await fetch_single_job_post(raw_id, lang)
            if not job:
                job = await fetch_single_order(raw_id, lang)
            return job
        except Exception:
            return None

@sync_to_async
def check_job_status_in_db(raw_id: int, job_type: str, worker_telegram_id: int):
    """
    Ishning ayni paytdagi holatini tekshirish:
    status: 'ACTIVE', 'TAKEN', 'CLOSED'
    already_applied: bool
    """
    user = User.objects.filter(telegram_id=worker_telegram_id).first()
    if job_type == 'job_post':
        job = JobPost.objects.filter(id=raw_id).first()
        if not job:
            return {'status': 'CLOSED', 'already_applied': False, 'msg': 'E\'lon o\'chirilgan'}
        if job.status == JobPost.Status.PAUSED:
            return {'status': 'CLOSED', 'already_applied': False, 'msg': 'E\'lon vaqtincha to\'xtatilgan'}
        if job.status in [JobPost.Status.COMPLETED, JobPost.Status.CANCELLED]:
            return {'status': 'TAKEN', 'already_applied': False, 'msg': 'Ishchi topilgan / Yopilgan'}
            
        already_applied = False
        if user:
            already_applied = JobApplication.objects.filter(job_post=job, worker=user).exists()
            
        return {'status': 'ACTIVE', 'already_applied': already_applied, 'title': str(job)}
    else: # order
        ord = Order.objects.filter(id=raw_id).first()
        if not ord:
            return {'status': 'CLOSED', 'already_applied': False, 'msg': 'Buyurtma mavjud emas'}
        if ord.status != Order.Status.PENDING:
            return {'status': 'TAKEN', 'already_applied': False, 'msg': 'Ishchiga biriktirilgan yoki yakunlangan'}
        return {'status': 'ACTIVE', 'already_applied': False, 'title': ord.title}

@sync_to_async
def create_job_application_in_db(raw_id: int, job_type: str, worker_telegram_id: int, proposal_msg: str):
    """
    Usta tomonidan ishga topshirish so'rovini saqlash va ish beruvchiga bildirishnoma tayyorlash
    """
    worker = User.objects.filter(telegram_id=worker_telegram_id).first()
    if not worker:
        return False, "Foydalanuvchi topilmadi", None
        
    if job_type == 'job_post':
        job = JobPost.objects.select_related('employer', 'position', 'category').filter(id=raw_id).first()
        if not job:
            return False, "E'lon topilmadi yoki o'chirilgan", None
        if job.status != JobPost.Status.ACTIVE:
            return False, "Ushbu e'lon faol emas yoki yopilgan", None
            
        app = JobApplication.objects.filter(job_post=job, worker=worker).first()
        if not app:
            app = JobApplication.objects.create(
                job_post=job,
                worker=worker,
                status=JobApplication.Status.PENDING,
                proposal_message=proposal_msg,
                is_deleted_by_worker=False
            )
        else:
            if app.proposal_message and not app.is_invited and app.status != JobApplication.Status.PENDING:
                return False, "Siz allaqachon ushbu ishga so'rov yuborgansiz", None
            app.status = JobApplication.Status.PENDING
            app.proposal_message = proposal_msg
            app.is_deleted_by_worker = False
            app.save(update_fields=['status', 'proposal_message', 'is_deleted_by_worker'])
            
        job.applications_count = job.applications.count()
        job.save(update_fields=['applications_count'])
        
        employer_tg_id = job.employer.telegram_id if job.employer else None
        return True, "So'rov muvaffaqiyatli yuborildi", {
            'employer_tg_id': employer_tg_id,
            'job_title': job.position.get_name('uz') if job.position else (job.custom_position_name or 'Ish'),
            'job_id': job.id,
            'worker_name': worker.get_full_name() or worker.first_name,
            'worker_phone': worker.phone_number,
            'proposal_msg': proposal_msg
        }
    else: # order
        ord = Order.objects.filter(id=raw_id).first()
        if not ord or ord.status != Order.Status.PENDING:
            return False, "Buyurtma boshqa ishchiga biriktirilgan yoki faol emas", None
        return True, "So'rov qabul qilindi", None

@sync_to_async
def get_worker_applications(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return []
    return list(
        JobApplication.objects.filter(worker=user, is_deleted_by_worker=False)
        .select_related('job_post', 'job_post__employer', 'job_post__position', 'job_post__category', 'job_post__region')
        .order_by('-applied_at')[:50]
    )

@sync_to_async
def delete_worker_application_in_db(app_id: int, worker_tg_id: int):
    app = JobApplication.objects.filter(id=app_id, worker__telegram_id=worker_tg_id).first()
    if app:
        app.is_deleted_by_worker = True
        app.save(update_fields=['is_deleted_by_worker'])
        return True
    return False

@sync_to_async
def get_worker_application_detail(app_id: int, telegram_id: int):
    app = (
        JobApplication.objects.select_related(
            'job_post', 'job_post__employer', 'job_post__position', 'job_post__category', 'job_post__region', 'worker'
        )
        .filter(id=app_id, worker__telegram_id=telegram_id)
        .first()
    )
    if not app:
        return None
        
    job = app.job_post
    employer = job.employer
    lang = app.worker.language or 'uz'
    
    pos_name = job.position.get_name(lang) if job.position else (job.custom_position_name or 'Ish')
    cat_name = job.category.get_name(lang) if job.category else 'Boshqa'
    
    # Location
    loc_parts = []
    if job.region:
        loc_parts.append(job.region.get_name(lang))
    if job.district:
        loc_parts.append(job.district)
    if job.address:
        loc_parts.append(job.address)
    loc_display = ", ".join(loc_parts) if loc_parts else "Ko'rsatilmagan"
    
    # Price
    if job.is_price_negotiable and not job.price_amount:
        price_display = "🤝 Narxi kelishiladi"
    elif job.price_amount:
        price_display = f"💰 {job.price_amount}"
    else:
        price_display = "🤝 Kelishiladi"
        
    # Start time
    if job.start_time_type == JobPost.StartTimeType.URGENT:
        time_display = "🔥 Tezkor (Bugun)"
    elif job.start_time_type == JobPost.StartTimeType.TOMORROW:
        time_display = "🗓 Ertaga"
    else:
        time_display = job.custom_start_date or "Kelishilgan vaqtda"
        
    return {
        'id': app.id,
        'status': app.status,
        'is_invited': app.is_invited,
        'applied_at': app.applied_at.strftime("%d.%m.%Y %H:%M") if app.applied_at else "",
        'proposal_message': app.proposal_message or "Taklif xabari kiritilmagan",
        'job_id': job.id,
        'job_title': pos_name,
        'category': cat_name,
        'address': loc_display,
        'price': price_display,
        'work_time': time_display,
        'work_format': job.get_employment_type_display(),
        'desc': job.description or "Batafsil ma'lumot berilmagan",
        'employer_name': job.contact_name or (employer.first_name if employer else 'Ish beruvchi'),
        'employer_phone': job.contact_phone or (employer.phone_number if employer else "Ko'rsatilmagan"),
        'employer_username': job.contact_telegram_username or (employer.username if employer else ''),
    }

@sync_to_async
def get_bot_settings_info():
    config = BotConfig.get_config()
    return {
        'call_center_phone': config.call_center_phone or '+998 (71) 200-00-00',
        'app_url': config.app_url or '',
        'app_url_enabled': bool(config.app_url_enabled and config.app_url),
        'about_text': config.about_text or '',
    }

# ==================== 0-DAN 5-GATON RO'YXATDAN O'TISH ====================

async def start_targeted_profile_update_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    user = update.effective_user
    queue = context.user_data.get('profile_update_queue', [])
    
    field_labels = {
        'name': "👤 Ism va familiya",
        'phone': "📱 Telefon raqam",
        'location': "📍 Joylashuv / Manzil",
        'positions': "🛠 Soha va mutaxassislik",
        'gender_age': "⚧ Yoshi va jinsi",
        'gender': "⚧ Jinsi",
        'age': "🎂 Yoshi",
        'work_schedule': "⏱ Ish rejimi",
    }
    
    human_fields = ", ".join([field_labels.get(f, f) for f in queue])
    intro_msg = (
        f"ℹ️ <b>Profil ma'lumotlarini yangilash</b>\n\n"
        f"Hurmatli <b>{user.first_name}</b>, iltimos quyidagi ma'lumotni yangilang:\n"
        f"👉 <b>{human_fields}</b>"
    )
    if update.message:
        await update.message.reply_text(intro_msg, parse_mode='HTML')
    elif update.callback_query:
        await update.callback_query.message.reply_text(intro_msg, parse_mode='HTML')
        
    return await next_profile_update_step(update, context)

async def next_profile_update_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    queue = context.user_data.get('profile_update_queue', [])
    
    if not queue:
        # Barcha talab qilingan maydonlar to'ldirildi! DBga saqlaymiz va tugatamiz
        user_id = update.effective_user.id
        username = update.effective_user.username or ''
        await save_full_profile_to_db(user_id, username, context.user_data)
        context.user_data.pop('is_targeted_profile_update', None)
        context.user_data.pop('profile_update_queue', None)
        
        success_text = "✅ <b>Profilingiz muvaffaqiyatli yangilandi va faollashtirildi!</b>"
        if update.message:
            await update.message.reply_text(success_text, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        elif update.callback_query:
            await update.callback_query.message.reply_text(success_text, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
            
        return await show_main_menu(update, context)
        
    next_field = queue[0]
    msg_target = update.message if update.message else update.callback_query.message
    
    if next_field == 'name':
        await msg_target.reply_text(t('step1_name_title', lang), reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        return STATE_FULL_NAME
        
    elif next_field in ('gender_age', 'gender'):
        keyboard = [
            [
                InlineKeyboardButton(t('gender_male', lang), callback_data="gender_male"),
                InlineKeyboardButton(t('gender_female', lang), callback_data="gender_female"),
            ]
        ]
        await msg_target.reply_text(t('step1_gender_title', lang), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return STATE_GENDER
        
    elif next_field == 'age':
        await msg_target.reply_text(t('step1_age_title', lang), reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        return STATE_AGE
        
    elif next_field == 'phone':
        keyboard = [[KeyboardButton(t('btn_send_phone', lang), request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await msg_target.reply_text(t('step1_phone_title', lang), reply_markup=reply_markup, parse_mode='HTML')
        return STATE_PHONE
        
    elif next_field == 'location':
        keyboard = [
            [KeyboardButton(t('btn_send_gps', lang), request_location=True)],
            [KeyboardButton(t('btn_manual_region', lang))]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await msg_target.reply_text(t('step2_geo_title', lang), reply_markup=reply_markup, parse_mode='HTML')
        return STATE_GEO_LOCATION
        
    elif next_field == 'positions':
        return await show_categories_page(msg_target, context, page=1)
        
    elif next_field == 'work_schedule':
        keyboard = [
            [InlineKeyboardButton(t('schedule_day', lang), callback_data="sched_day_shift")],
            [InlineKeyboardButton(t('schedule_24_7', lang), callback_data="sched_24_7")],
            [InlineKeyboardButton(t('schedule_flexible', lang), callback_data="sched_flexible")],
        ]
        await msg_target.reply_text(t('step4_schedule_title', lang), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return STATE_WORK_SCHEDULE
        
    else:
        queue.pop(0)
        context.user_data['profile_update_queue'] = queue
        return await next_profile_update_step(update, context)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = await get_user_db_record(user.id)
    
    # 1. Agar foydalanuvchi ma'lumotlarini qisman yangilash talab qilingan bo'lsa
    if db_user and db_user.get('needs_profile_update') and db_user.get('has_existing_profile'):
        lang = db_user['language'] or 'uz'
        context.user_data['lang'] = lang
        profile = await get_user_profile(user.id)
        if profile:
            context.user_data['full_name'] = profile.get('name', '')
            context.user_data['phone'] = profile.get('phone', '')
            context.user_data['gender'] = 'male' if profile.get('gender') != 'female' else 'female'
            context.user_data['age'] = profile.get('age', 25)
            context.user_data['region_id'] = profile.get('region_id')
            context.user_data['latitude'] = profile.get('latitude')
            context.user_data['longitude'] = profile.get('longitude')
            context.user_data['district'] = profile.get('district', '')
            context.user_data['street_address'] = profile.get('street_address', '')
            context.user_data['category_id'] = profile.get('category_id')
            context.user_data['work_schedule'] = '24_7'
            context.user_data['selected_pos_ids'] = set()
            
        raw_fields = db_user.get('profile_update_fields', '')
        fields = [f.strip() for f in raw_fields.split(',') if f.strip() and f.strip() != 'all']
        if not fields:
            fields = ['name', 'phone', 'location', 'positions']
        context.user_data['profile_update_queue'] = fields
        context.user_data['is_targeted_profile_update'] = True
        
        return await start_targeted_profile_update_flow(update, context)

    # 2. Agar foydalanuvchi allaqachon to'liq ro'yxatdan o'tgan bo'lsa -> To'g'ridan to'g'ri kutib olib Asosiy Menyuni ochish
    if db_user and db_user['is_registered']:
        lang = db_user['language']
        context.user_data['lang'] = lang
        profile = await get_user_profile(user.id)
        welcome_msg = t('welcome_back', lang, name=profile['name'])
        if update.message:
            await update.message.reply_text(welcome_msg, parse_mode='HTML')
        elif update.callback_query:
            await update.callback_query.message.reply_text(welcome_msg, parse_mode='HTML')
        return await show_main_menu(update, context)
        
    # 3. Yangi foydalanuvchi -> DBda darhol Lid sifatida saqlash va 0-qadam Til tanlash
    await record_lead_worker(
        telegram_id=user.id,
        username=user.username or '',
        first_name=user.first_name or '',
        last_name=user.last_name or '',
        lang='uz'
    )

    context.user_data.clear()
    context.user_data['selected_pos_ids'] = set()
    
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha (Lotin)", callback_data="lang_uz"),
            InlineKeyboardButton("🇺🇿 Ўзбекча (Крилл)", callback_data="lang_oz"),
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        from bot_control.models import BotConfig
        proj_name = await sync_to_async(BotConfig.get_project_name)()
    except Exception:
        proj_name = "IshBazari"

    msg_text = (
        f"👋 Assalomu alaykum! <b>{proj_name}</b> rasmiy botiga xush kelibsiz.\n"
        "Iltimos, muloqot tilini tanlang:\n\n"
        "Пожалуйста, выберите язык:\n\n"
        "Please choose your language:"
    )
    
    if update.message:
        await update.message.reply_text(msg_text, reply_markup=reply_markup, parse_mode='HTML')
    elif update.callback_query:
        await update.callback_query.message.edit_text(msg_text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_LANGUAGE

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang = query.data.replace("lang_", "")
    context.user_data['lang'] = lang
    
    # Lidning tanlagan tilini DBda ham yangilash
    user = update.effective_user
    await record_lead_worker(
        telegram_id=user.id,
        username=user.username or '',
        first_name=user.first_name or '',
        last_name=user.last_name or '',
        lang=lang
    )
    
    # 0.1-QADAM: ROLNI TANLASH
    keyboard = [
        [InlineKeyboardButton(t('role_worker', lang), callback_data="role_worker")],
        [InlineKeyboardButton(t('role_client', lang), callback_data="role_client")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"{t('lang_selected', lang)}\n\n{t('choose_role', lang)}"
    await query.message.edit_text(text, reply_markup=reply_markup)
    return STATE_ROLE

async def role_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    role_type = query.data.replace("role_", "")
    lang = context.user_data.get('lang', 'uz')
    
    if role_type == 'client':
        try:
            client_bot_url = await sync_to_async(BotConfig.get_client_bot_link)()
        except Exception as e:
            logger.error(f"Error getting client_bot_link: {e}")
            client_bot_url = "https://t.me/ishjoyla_bot?start=ref_worker_bot"

        keyboard = [
            [InlineKeyboardButton(t('btn_goto_client_bot', lang), url=client_bot_url)],
            [InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_lang")]
        ]
        await query.message.edit_text(
            t('client_redirect_msg', lang), 
            reply_markup=InlineKeyboardMarkup(keyboard), 
            parse_mode='HTML'
        )
        return STATE_ROLE
        
    context.user_data['role'] = User.Role.WORKER
    
    # 1.1-QADAM: JINSNI TANLASH
    keyboard = [
        [
            InlineKeyboardButton(t('gender_male', lang), callback_data="gender_male"),
            InlineKeyboardButton(t('gender_female', lang), callback_data="gender_female"),
        ],
        [InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_role")]
    ]
    await query.message.edit_text(t('step1_gender_title', lang), reply_markup=InlineKeyboardMarkup(keyboard))
    return STATE_GENDER

async def gender_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    if data == "back_to_role":
        keyboard = [
            [InlineKeyboardButton(t('role_worker', lang), callback_data="role_worker")],
            [InlineKeyboardButton(t('role_client', lang), callback_data="role_client")],
        ]
        await query.message.edit_text(t('choose_role', lang), reply_markup=InlineKeyboardMarkup(keyboard))
        return STATE_ROLE
        
    gender = 'male' if data == 'gender_male' else 'female'
    context.user_data['gender'] = gender
    
    if context.user_data.get('is_targeted_profile_update'):
        queue = context.user_data.get('profile_update_queue', [])
        if 'gender_age' in queue:
            await query.message.reply_text(t('step1_age_title', lang), parse_mode='HTML')
            return STATE_AGE
        elif 'gender' in queue:
            queue.remove('gender')
            context.user_data['profile_update_queue'] = queue
            return await next_profile_update_step(update, context)
            
    await query.message.edit_text(t('step1_name_title', lang), parse_mode='HTML')
    return STATE_FULL_NAME

async def full_name_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    lang = context.user_data.get('lang', 'uz')
    
    if len(name) < 2:
        await update.message.reply_text(t('step1_name_title', lang), parse_mode='HTML')
        return STATE_FULL_NAME
        
    context.user_data['full_name'] = name
    
    if context.user_data.get('is_targeted_profile_update'):
        queue = context.user_data.get('profile_update_queue', [])
        if 'name' in queue:
            queue.remove('name')
        context.user_data['profile_update_queue'] = queue
        return await next_profile_update_step(update, context)
        
    await update.message.reply_text(t('step1_age_title', lang), parse_mode='HTML')
    return STATE_AGE

async def age_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    lang = context.user_data.get('lang', 'uz')
    
    if not text.isdigit() or int(text) < 14 or int(text) > 100:
        await update.message.reply_text(t('step1_age_invalid', lang))
        return STATE_AGE
        
    context.user_data['age'] = int(text)
    
    if context.user_data.get('is_targeted_profile_update'):
        queue = context.user_data.get('profile_update_queue', [])
        if 'gender_age' in queue:
            queue.remove('gender_age')
        if 'age' in queue:
            queue.remove('age')
        context.user_data['profile_update_queue'] = queue
        return await next_profile_update_step(update, context)
        
    # 1.4: Telefon raqam
    keyboard = [[KeyboardButton(t('btn_send_phone', lang), request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(t('step1_phone_title', lang), reply_markup=reply_markup)
    return STATE_PHONE

async def phone_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number if contact else update.message.text.strip()
    lang = context.user_data.get('lang', 'uz')
    
    clean_phone = re.sub(r'[^0-9+]', '', phone)
    if not clean_phone.startswith('+'):
        clean_phone = '+' + clean_phone
        
    if len(clean_phone) < 9:
        await update.message.reply_text(t('step1_phone_invalid', lang))
        return STATE_PHONE
        
    context.user_data['phone'] = clean_phone
    
    if context.user_data.get('is_targeted_profile_update'):
        queue = context.user_data.get('profile_update_queue', [])
        if 'phone' in queue:
            queue.remove('phone')
        context.user_data['profile_update_queue'] = queue
        return await next_profile_update_step(update, context)
        
    # 2.1: GPS Lokatsiya
    keyboard = [
        [KeyboardButton(t('btn_send_gps', lang), request_location=True)],
        [KeyboardButton(t('btn_manual_region', lang))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(t('step2_geo_title', lang), reply_markup=reply_markup, parse_mode='HTML')
    return STATE_GEO_LOCATION

async def geo_location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    
    if update.message.text and (t('btn_manual_region', lang) in update.message.text or "qo'lda" in update.message.text.lower() or "қўлда" in update.message.text.lower()):
        regions = await get_active_regions(lang)
        keyboard = []
        row = []
        for reg_id, reg_name in regions:
            row.append(InlineKeyboardButton(reg_name, callback_data=f"reg_{reg_id}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(t('choose_region_worker', lang), reply_markup=reply_markup)
        return STATE_MANUAL_REGION
        
    loc = update.message.location
    if loc:
        lat, lon = loc.latitude, loc.longitude
        context.user_data['latitude'] = lat
        context.user_data['longitude'] = lon
        
        # Reverse Geocoding (vaqtinchalik xotiraga)
        geo_info = await save_location_from_gps(None, lat, lon)
        if geo_info.get('region_id'):
            context.user_data['region_id'] = geo_info['region_id']
        context.user_data['district'] = geo_info.get('district', '')
        context.user_data['region_name'] = geo_info.get('region_name', '')
        
        detected_text = f"📍 <b>Aniqlangan hudud:</b> {geo_info.get('region_name', '')}, {geo_info.get('district', '')}"
        await update.message.reply_text(detected_text, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        await update.message.reply_text(t('step2_address_title', lang), parse_mode='HTML')
        return STATE_STREET_ADDRESS
        
    await update.message.reply_text(t('step2_geo_title', lang), parse_mode='HTML')
    return STATE_GEO_LOCATION

async def manual_region_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    region_id = int(data.replace("reg_", ""))
    context.user_data['region_id'] = region_id
    
    await query.message.edit_text(t('step2_address_title', lang), parse_mode='HTML')
    return STATE_STREET_ADDRESS

async def street_address_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()
    context.user_data['street_address'] = address
    
    if context.user_data.get('is_targeted_profile_update'):
        queue = context.user_data.get('profile_update_queue', [])
        if 'location' in queue:
            queue.remove('location')
        context.user_data['profile_update_queue'] = queue
        return await next_profile_update_step(update, context)
        
    return await show_categories_page(update, context, page=1)

async def show_categories_page(update_or_query, context: ContextTypes.DEFAULT_TYPE, page: int = 1):
    lang = context.user_data.get('lang', 'uz')
    categories, cur_page, total_pages = await get_categories_page(lang=lang, page=page)
    context.user_data['cat_page'] = cur_page
    selected_set = context.user_data.setdefault('selected_pos_ids', set())
    
    keyboard = []
    row = []
    for cat_id, cat_name in categories:
        row.append(InlineKeyboardButton(cat_name, callback_data=f"cat_{cat_id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    prev_cb = f"catpage_{cur_page - 1}" if cur_page > 1 else "noop"
    next_cb = f"catpage_{cur_page + 1}" if cur_page < total_pages else "noop"
    prev_text = "◀️" if cur_page > 1 else "▫️"
    next_text = "▶️" if cur_page < total_pages else "▫️"
    page_text = f"📄 {cur_page} / {total_pages}"
    
    keyboard.append([
        InlineKeyboardButton(prev_text, callback_data=prev_cb),
        InlineKeyboardButton(page_text, callback_data="noop"),
        InlineKeyboardButton(next_text, callback_data=next_cb),
    ])
    
    if selected_set:
        keyboard.append([
            InlineKeyboardButton(t('btn_continue', lang, count=len(selected_set)), callback_data="pos_done")
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = t('choose_category', lang, current=cur_page, total=total_pages)
    if selected_set:
        text += f"\n\n<i>Tanlangan mutaxassisliklar: {len(selected_set)}/10 ta</i>"
    
    if hasattr(update_or_query, 'message') and update_or_query.message and not hasattr(update_or_query, 'data'):
        await update_or_query.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    elif hasattr(update_or_query, 'edit_text'):
        await update_or_query.edit_text(text, reply_markup=reply_markup, parse_mode='HTML')
    elif getattr(update_or_query, 'callback_query', None):
        await update_or_query.callback_query.message.edit_text(text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_CATEGORY

async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    
    if data.startswith("catpage_"):
        page = int(data.replace("catpage_", ""))
        return await show_categories_page(query.message, context, page=page)
    
    if data == "noop":
        return STATE_CATEGORY
        
    if data == "pos_done":
        if context.user_data.get('is_targeted_profile_update'):
            queue = context.user_data.get('profile_update_queue', [])
            if 'positions' in queue:
                queue.remove('positions')
            context.user_data['profile_update_queue'] = queue
            return await next_profile_update_step(update, context)
        return await show_employment_type_step(query.message, context)
        
    if data.startswith("cat_"):
        cat_id = int(data.replace("cat_", ""))
        context.user_data['category_id'] = cat_id
        return await show_positions_page(query.message, context, category_id=cat_id, page=1)

    return STATE_CATEGORY

async def show_positions_page(msg_or_query, context: ContextTypes.DEFAULT_TYPE, category_id: int, page: int = 1):
    lang = context.user_data.get('lang', 'uz')
    positions, cur_page, total_pages = await get_positions_page(category_id=category_id, lang=lang, page=page)
    context.user_data['pos_page'] = cur_page
    
    selected_set = context.user_data.setdefault('selected_pos_ids', set())
    
    keyboard = []
    row = []
    for pos_id, pos_name in positions:
        is_selected = pos_id in selected_set
        btn_label = f"✅ {pos_name}" if is_selected else f"⬜ {pos_name}"
        row.append(InlineKeyboardButton(btn_label, callback_data=f"pos_{pos_id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    prev_cb = f"pospage_{cur_page - 1}" if cur_page > 1 else "noop"
    next_cb = f"pospage_{cur_page + 1}" if cur_page < total_pages else "noop"
    prev_text = "◀️" if cur_page > 1 else "▫️"
    next_text = "▶️" if cur_page < total_pages else "▫️"
    page_text = f"📄 {cur_page} / {total_pages}"
    
    keyboard.append([
        InlineKeyboardButton(prev_text, callback_data=prev_cb),
        InlineKeyboardButton(page_text, callback_data="noop"),
        InlineKeyboardButton(next_text, callback_data=next_cb),
    ])
    
    if selected_set:
        keyboard.append([
            InlineKeyboardButton(t('btn_continue', lang, count=len(selected_set)), callback_data="pos_done")
        ])
        
    keyboard.append([
        InlineKeyboardButton(t('btn_choose_other_cats', lang), callback_data="back_to_cat_list"),
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = t('choose_position', lang, current=cur_page, total=total_pages, selected_count=len(selected_set))
    
    if hasattr(msg_or_query, 'edit_text'):
        await msg_or_query.edit_text(text, reply_markup=reply_markup)
    else:
        await msg_or_query.reply_text(text, reply_markup=reply_markup)
    return STATE_POSITION

async def position_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    cat_id = context.user_data.get('category_id')
    selected_set = context.user_data.setdefault('selected_pos_ids', set())
    
    if data.startswith("pospage_"):
        await query.answer()
        page = int(data.replace("pospage_", ""))
        return await show_positions_page(query.message, context, category_id=cat_id, page=page)
        
    if data == "noop":
        await query.answer()
        return STATE_POSITION
        
    if data == "back_to_cat_list":
        await query.answer()
        return await show_categories_page(query.message, context, page=context.user_data.get('cat_page', 1))
        
    if data == "pos_done":
        await query.answer()
        return await show_employment_type_step(query.message, context)
        
    if data.startswith("pos_"):
        pos_id = int(data.replace("pos_", ""))
        if pos_id in selected_set:
            selected_set.remove(pos_id)
            await query.answer("O'chirildi")
        else:
            if len(selected_set) >= 10:
                await query.answer(t('max_pos_alert', lang), show_alert=True)
                return STATE_POSITION
            selected_set.add(pos_id)
            await query.answer(f"Tanlandi ({len(selected_set)}/10)")
            
        return await show_positions_page(query.message, context, category_id=cat_id, page=context.user_data.get('pos_page', 1))

    return STATE_POSITION

async def show_employment_type_step(msg_target, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    keyboard = [
        [InlineKeyboardButton(t('emp_type_daily', lang), callback_data="emp_daily")],
        [InlineKeyboardButton(t('emp_type_permanent', lang), callback_data="emp_permanent")],
        [InlineKeyboardButton(t('emp_type_both', lang), callback_data="emp_both")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = t('step4_emp_type_title', lang)
    if hasattr(msg_target, 'edit_text'):
        await msg_target.edit_text(text, reply_markup=reply_markup)
    else:
        await msg_target.reply_text(text, reply_markup=reply_markup)
    return STATE_EMPLOYMENT_TYPE

async def employment_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    emp_type = query.data.replace("emp_", "")
    context.user_data['employment_type'] = emp_type
    
    lang = context.user_data.get('lang', 'uz')
    keyboard = [
        [InlineKeyboardButton(t('schedule_day', lang), callback_data="sched_day_shift")],
        [InlineKeyboardButton(t('schedule_24_7', lang), callback_data="sched_24_7")],
        [InlineKeyboardButton(t('schedule_flexible', lang), callback_data="sched_flexible")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(t('step4_schedule_title', lang), reply_markup=reply_markup)
    return STATE_WORK_SCHEDULE

async def work_schedule_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    sched = query.data.replace("sched_", "")
    context.user_data['work_schedule'] = sched
    
    if context.user_data.get('is_targeted_profile_update'):
        queue = context.user_data.get('profile_update_queue', [])
        if 'work_schedule' in queue:
            queue.remove('work_schedule')
        context.user_data['profile_update_queue'] = queue
        return await next_profile_update_step(update, context)
        
    return await show_review_card(query.message, context)

async def show_review_card(msg_target, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    user_data = context.user_data
    
    gender_map = {'male': t('gender_male', lang), 'female': t('gender_female', lang)}
    emp_map = {'daily': t('emp_type_daily', lang), 'permanent': t('emp_type_permanent', lang), 'both': t('emp_type_both', lang)}
    sched_map = {'day_shift': t('schedule_day', lang), '24_7': t('schedule_24_7', lang), 'flexible': t('schedule_flexible', lang)}
    
    reg_id = user_data.get('region_id')
    region_name = user_data.get('region_name', '')
    if reg_id and not region_name:
        r = await sync_to_async(Region.objects.filter(id=reg_id).first)()
        region_name = r.get_name(lang) if r else "O'zbekiston"
        
    cat_id = user_data.get('category_id')
    cat_name = user_data.get('custom_category', '')
    if cat_id and not cat_name:
        c = await sync_to_async(Category.objects.filter(id=cat_id).first)()
        cat_name = c.get_name(lang) if c else 'Tanlanmagan'
        
    pos_ids = list(user_data.get('selected_pos_ids', []))
    if pos_ids:
        pos_objs = await sync_to_async(list)(Position.objects.filter(id__in=pos_ids))
        pos_names = [p.get_name(lang) for p in pos_objs]
        pos_str = ", ".join(pos_names)
        pos_count = len(pos_names)
    elif user_data.get('custom_position'):
        pos_str = user_data.get('custom_position')
        pos_count = 1
    else:
        pos_str = 'Tanlanmagan'
        pos_count = 0
        
    card_text = t(
        'step5_review_title',
        lang,
        name=user_data.get('full_name', 'Foydalanuvchi'),
        gender=gender_map.get(user_data.get('gender'), 'Erkak'),
        age=user_data.get('age', 25),
        phone=user_data.get('phone', 'Mavjud emas'),
        region=region_name or "O'zbekiston",
        district=user_data.get('district', ''),
        street_address=user_data.get('street_address', 'Kiritilmagan'),
        category=cat_name,
        positions=pos_str,
        pos_count=pos_count,
        emp_type=emp_map.get(user_data.get('employment_type'), 'Ikkalasi ham'),
        work_schedule=sched_map.get(user_data.get('work_schedule'), 'Erkin grafik')
    )
    
    keyboard = [
        [InlineKeyboardButton(t('btn_confirm_profile', lang), callback_data="confirm_save")],
        [InlineKeyboardButton(t('btn_restart_profile', lang), callback_data="restart_flow")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if hasattr(msg_target, 'edit_text'):
        await msg_target.edit_text(card_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await msg_target.reply_text(card_text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_CONFIRM_PROFILE

async def confirm_profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    lang = context.user_data.get('lang', 'uz')
    user = query.from_user
    
    if data == "restart_flow":
        # Tilni saqlab qolgan holda 1-qadam (Shaxsiy ma'lumotlar / Jins)dan boshlash
        saved_lang = context.user_data.get('lang', 'uz')
        context.user_data.clear()
        context.user_data['lang'] = saved_lang
        context.user_data['role'] = User.Role.WORKER
        context.user_data['selected_pos_ids'] = set()
        
        keyboard = [
            [
                InlineKeyboardButton(t('gender_male', saved_lang), callback_data="gender_male"),
                InlineKeyboardButton(t('gender_female', saved_lang), callback_data="gender_female"),
            ],
            [InlineKeyboardButton(t('btn_back', saved_lang), callback_data="back_to_role")]
        ]
        await query.message.edit_text(t('step1_gender_title', saved_lang), reply_markup=InlineKeyboardMarkup(keyboard))
        return STATE_GENDER
        
    if data == "confirm_save":
        await save_full_profile_to_db(user.id, user.username or '', context.user_data)
        await query.message.reply_text(t('reg_success', lang), reply_markup=ReplyKeyboardRemove())
        return await show_main_menu(update, context)
        
    return STATE_CONFIRM_PROFILE

# ==================== ASOSIY BOSH MENYU VA BO'LIMLAR ====================

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    profile = await get_user_profile(user_id)
    lang = profile['lang_code'] if profile else context.user_data.get('lang', 'uz')
    context.user_data['lang'] = lang
    
    status_badge = t('status_busy_badge', lang) if profile and profile.get('is_busy') else t('status_active_badge', lang)
    
    apps = await get_worker_applications(user_id)
    apps_count = len(apps)
    apps_badge = f" ({apps_count})" if apps_count > 0 else ""
    
    keyboard = [
        [InlineKeyboardButton(t('btn_menu_jobs', lang), callback_data="menu_jobs")],
        [
            InlineKeyboardButton(t('btn_menu_profile', lang), callback_data="menu_profile"),
            InlineKeyboardButton(f"👥 {t('btn_menu_applications', lang)}{apps_badge}", callback_data="menu_my_applications"),
        ],
        [
            InlineKeyboardButton(t('btn_menu_update_gps', lang), callback_data="menu_update_gps"),
            InlineKeyboardButton(t('btn_menu_toggle_status', lang), callback_data="menu_toggle_status"),
        ],
        [
            InlineKeyboardButton(t('btn_menu_reviews', lang), callback_data="menu_reviews"),
            InlineKeyboardButton(t('btn_menu_settings', lang), callback_data="menu_settings"),
        ],
        [
            InlineKeyboardButton(t('btn_menu_support', lang), callback_data="menu_support"),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Hudud va tuman matnini chiroyli shakllantiramiz: masalan "Farg'ona viloyati, Quva tumani"
    loc_str = "Tanlanmagan"
    if profile:
        reg = profile.get('region') or ''
        dist = profile.get('district') or ''
        if reg and reg != 'Tanlanmagan' and dist:
            loc_str = f"{reg}, {dist}"
        elif reg and reg != 'Tanlanmagan':
            loc_str = reg
        elif dist:
            loc_str = dist
            
    msg_text = t(
        'main_menu', 
        lang,
        name=profile['name'] if profile else 'Usta',
        positions=profile['positions'] if profile else 'Tanlanmagan',
        location=loc_str,
        status_badge=status_badge
    )
    
    if update.message:
        await update.message.reply_text(msg_text, reply_markup=reply_markup, parse_mode='HTML')
    elif update.callback_query:
        await update.callback_query.message.edit_text(msg_text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU

# ==================== JAVOBLAR (YUBORILGAN SO'ROVLAR) ====================

WORKER_APP_PAGE_SIZE = 6

async def worker_applications_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0):
    query = update.callback_query
    if query:
        await query.answer()
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    
    apps = await get_worker_applications(user_id)
    if not apps:
        keyboard = [[InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")]]
        msg = t('my_applications_empty', lang)
        if query and query.message:
            await query.message.edit_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        else:
            await update.effective_message.reply_text(text=msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return STATE_MAIN_MENU

    total_pages = max(1, (len(apps) + WORKER_APP_PAGE_SIZE - 1) // WORKER_APP_PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))
    
    start_idx = page * WORKER_APP_PAGE_SIZE
    page_apps = apps[start_idx:start_idx + WORKER_APP_PAGE_SIZE]

    text = t('my_applications_title', lang, count=len(apps), current=page+1, total=total_pages)
    keyboard = []
    for a in page_apps:
        job_title = a.job_post.position.get_name(lang) if a.job_post.position else (a.job_post.custom_position_name or 'Ish')
        status_icon = "⏳" if a.status == JobApplication.Status.PENDING else ("✅" if a.status == JobApplication.Status.ACCEPTED else "❌")
        btn_title = f"{status_icon} #{a.job_post_id} {job_title} ({a.job_post.district or 'Hudud'})"
        keyboard.append([InlineKeyboardButton(btn_title, callback_data=f"my_app_view_{a.id}")])
        
    nav_btns = []
    if page > 0:
        nav_btns.append(InlineKeyboardButton("⬅️", callback_data=f"my_app_page_{page-1}"))
    if total_pages > 1:
        nav_btns.append(InlineKeyboardButton(f"📄 {page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_btns.append(InlineKeyboardButton("➡️", callback_data=f"my_app_page_{page+1}"))
    if nav_btns:
        keyboard.append(nav_btns)
        
    keyboard.append([InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query and query.message:
        await query.message.edit_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.effective_message.reply_text(text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU

async def worker_application_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, app_id: int):
    query = update.callback_query
    if query:
        await query.answer()
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    
    detail = await get_worker_application_detail(app_id, user_id)
    if not detail:
        if query:
            await query.answer("So'rov topilmadi yoki o'chirilgan!", show_alert=True)
        return await show_main_menu(update, context)
        
    status_label = "⏳ Kutilmoqda (Ko'rib chiqilmoqda)" if detail['status'] == 'pending' else ("✅ Qabul qilingan" if detail['status'] == 'accepted' else "❌ Rad etilgan")
    
    # Agar qabul qilingan bo'lsa -> Ish beruvchining kontaktlari to'liq ko'rinadi
    contact_section = ""
    if detail['status'] == 'accepted':
        tg_link = f"@{detail['employer_username']}" if detail['employer_username'] else "Mavjud emas"
        contact_section = (
            f"\n\n🔓 <b>ISH BERUVCHI (BUYURTMACHI) KONTAKTLARI:</b>\n"
            f"👤 <b>Mijoz:</b> {detail['employer_name']}\n"
            f"📞 <b>Telefon:</b> {detail['employer_phone']}\n"
            f"💬 <b>Telegram:</b> {tg_link}\n\n"
            f"<i>Ishni boshlash va tafsilotlarni kelishish uchun ish beruvchi bilan bog'laning!</i>"
        )
    else:
        contact_section = f"\n\n🔒 <i>Ish beruvchi so'rovingizni qabul qilishi bilan uning barcha aloqa ma'lumotlari ushbu joyda ochiladi.</i>"

    card_text = t(
        'my_app_detail_card',
        lang,
        job_id=detail['job_id'],
        job_title=detail['job_title'],
        status_label=status_label,
        applied_at=detail['applied_at'],
        address=detail['address'],
        price=detail['price'],
        work_time=detail['work_time'],
        work_format=detail['work_format'],
        desc=detail['desc'],
        proposal_msg=detail['proposal_message'],
        contact_section=contact_section
    )
    
    keyboard = []
    
    # Agar taklif qilingan ish bo'lsa va hali kutilayotgan bo'lsa -> Ishni qabul qilish / Taklif yuborish tugmasi
    if detail.get('is_invited') and detail['status'] == 'pending':
        keyboard.append([
            InlineKeyboardButton(t('btn_accept_invited_job', lang), callback_data=f"job_take_JP-{detail['job_id']}")
        ])
        
    # O'chirish tugmasi (ishchi o'zi uchun ro'yxatdan o'chiradi)
    keyboard.append([
        InlineKeyboardButton(t('btn_delete_application', lang), callback_data=f"my_app_del_{detail['id']}")
    ])
    
    keyboard.append([InlineKeyboardButton("⬅️ So'rovlar ro'yxatiga qaytish", callback_data="menu_my_applications")])
    keyboard.append([InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query and query.message:
        await query.message.edit_text(text=card_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.effective_message.reply_text(text=card_text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU

# ==================== 1. ISHLARNI KO'RISH / QIDIRISH ====================

async def show_jobs_sub_menu(query, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    keyboard = [
        [InlineKeyboardButton(t('btn_jobs_matched', lang), callback_data="jobs_matched")],
        [InlineKeyboardButton(t('btn_jobs_by_cat', lang), callback_data="jobs_by_cat")],
        [InlineKeyboardButton(t('btn_jobs_by_geo', lang), callback_data="jobs_by_geo")],
        [InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")],
    ]
    await query.message.edit_text(t('jobs_menu_title', lang), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

async def show_job_card(query, context: ContextTypes.DEFAULT_TYPE, job_index: int = 0):
    lang = context.user_data.get('lang', 'uz')
    jobs = context.user_data.get('current_jobs_list', [])
    
    if not jobs:
        keyboard = [
            [InlineKeyboardButton(t('btn_refresh_jobs', lang), callback_data="job_refresh")],
            [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_jobs")],
            [InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")],
        ]
        try:
            if hasattr(query, 'message') and query.message:
                await query.message.edit_text(t('jobs_empty', lang), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
            elif hasattr(query, 'edit_message_text'):
                await query.edit_message_text(t('jobs_empty', lang), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        except Exception as e:
            if "Message is not modified" not in str(e):
                logger.error(f"Error in show_job_card empty edit_text: {e}")
        return STATE_MAIN_MENU
        
    total = len(jobs)
    job_index = max(0, min(job_index, total - 1))
    context.user_data['job_index'] = job_index
    j = jobs[job_index]
    
    card_text = t(
        'job_card_text',
        lang,
        id=j['id'],
        current=job_index + 1,
        total=total,
        category=j['category'],
        service_type=j['service_type'],
        address=j['address'],
        work_time=j['work_time'],
        work_format=j['work_format'],
        price=j['price'],
        desc=j['desc'],
        customer_name=j['customer_name']
    )
    
    keyboard = [
        # 1. Asosiy harakat tugmalari: Ishni olish va Faolligini tekshirish
        [
            InlineKeyboardButton(t('btn_take_job', lang), callback_data=f"job_take_{j['id']}"),
            InlineKeyboardButton(t('btn_check_job_status', lang), callback_data=f"job_check_{j['id']}")
        ]
    ]
    
    # 2. Pagination qatori: ⬅️ Oldingi | 📌 current/total (qoldi: X) | Keyingi ➡️
    remaining = total - (job_index + 1)
    page_info_text = f"📄 {job_index + 1}/{total} (qoldi: {remaining})" if remaining > 0 else f"📄 {job_index + 1}/{total} (oxirgisi)"
    
    nav_row = [
        InlineKeyboardButton("⬅️", callback_data=f"job_nav_{job_index - 1}") if job_index > 0 else InlineKeyboardButton("⏺", callback_data="noop"),
        InlineKeyboardButton(page_info_text, callback_data="noop"),
        InlineKeyboardButton("➡️", callback_data=f"job_nav_{job_index + 1}") if job_index < total - 1 else InlineKeyboardButton("⏺", callback_data="noop"),
    ]
    keyboard.append(nav_row)
        
    # 3. Pastki qator: Orqaga va Yangilash
    keyboard.append([
        InlineKeyboardButton(t('btn_back', lang), callback_data="menu_jobs"),
        InlineKeyboardButton(t('btn_refresh_jobs', lang), callback_data="job_refresh"),
    ])
    
    try:
        if hasattr(query, 'message') and query.message:
            await query.message.edit_text(card_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        elif hasattr(query, 'edit_message_text'):
            await query.edit_message_text(card_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    except Exception as e:
        if "Message is not modified" not in str(e):
            logger.error(f"Error in show_job_card edit_text: {e}")
            
    return STATE_MAIN_MENU

# ==================== 2. MENING PROFILIM (KABINET) ====================

async def show_profile_cabinet(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id
    profile = await get_user_profile(user_id)
    lang = profile['lang_code'] if profile else context.user_data.get('lang', 'uz')
    
    status_badge = t('status_busy_badge', lang) if profile['is_busy'] else t('status_active_badge', lang)
    
    text = t(
        'cabinet_title',
        lang,
        name=profile['name'],
        age=profile['age'],
        gender=profile['gender'],
        phone=profile['phone'],
        region=profile['region'],
        district=profile['district'],
        street_address=profile['street_address'],
        positions=profile['positions'],
        pos_count=profile['pos_count'],
        work_schedule=profile['work_schedule'],
        emp_type=profile['emp_type'],
        status_badge=status_badge,
        rating=profile['rating'],
        reviews_count=profile['reviews_count'],
        completed_count=profile['completed_count']
    )
    
    keyboard = [
        [InlineKeyboardButton(t('btn_edit_profile', lang), callback_data="edit_profile_menu")],
        [InlineKeyboardButton(t('btn_portfolio', lang), callback_data="view_portfolio")],
        [InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")],
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

async def show_portfolio_menu(query_or_msg, context: ContextTypes.DEFAULT_TYPE):
    user_id = query_or_msg.from_user.id if hasattr(query_or_msg, 'from_user') and query_or_msg.from_user else (query_or_msg.chat_id if hasattr(query_or_msg, 'chat_id') else update.effective_user.id)
    lang = context.user_data.get('lang', 'uz')
    photos = await get_user_portfolio_photos(user_id)
    count = len(photos)
    context.user_data['user_portfolio_photos'] = photos
    
    text = t('portfolio_title', lang, count=count)
    keyboard = []
    
    if count < 5:
        keyboard.append([InlineKeyboardButton(t('btn_add_portfolio_item', lang), callback_data="portfolio_add")])
    if count > 0:
        keyboard.append([InlineKeyboardButton(t('btn_view_portfolio_items', lang, count=count), callback_data="portfolio_view_0")])
        
    keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="menu_profile")])
    keyboard.append([InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    if hasattr(query_or_msg, 'message') and query_or_msg.message:
        await query_or_msg.message.edit_text(text, reply_markup=reply_markup, parse_mode='HTML')
    elif hasattr(query_or_msg, 'edit_text'):
        await query_or_msg.edit_text(text, reply_markup=reply_markup, parse_mode='HTML')
    elif hasattr(query_or_msg, 'reply_text'):
        await query_or_msg.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        chat_id = query_or_msg.message.chat_id if hasattr(query_or_msg, 'message') and query_or_msg.message else user_id
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode='HTML')
    return STATE_MAIN_MENU

async def show_portfolio_card(query_or_msg, context: ContextTypes.DEFAULT_TYPE, index: int = 0):
    user_id = query_or_msg.from_user.id if hasattr(query_or_msg, 'from_user') and query_or_msg.from_user else (query_or_msg.chat_id if hasattr(query_or_msg, 'chat_id') else update.effective_user.id)
    lang = context.user_data.get('lang', 'uz')
    photos = await get_user_portfolio_photos(user_id)
    count = len(photos)
    
    if count == 0:
        return await show_portfolio_menu(query_or_msg, context)
        
    index = max(0, min(index, count - 1))
    item = photos[index]
    context.user_data['portfolio_view_index'] = index
    context.user_data['portfolio_current_item_id'] = item['id']
    
    caption_text = item['caption'] if item.get('caption') else t('portfolio_item_no_caption', lang)
    card_caption = t(
        'portfolio_item_card',
        lang,
        current=index + 1,
        total=count,
        caption=caption_text
    )
    
    keyboard = []
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton(t('btn_prev_item', lang), callback_data=f"portfolio_view_{index - 1}"))
    if index < count - 1:
        nav_row.append(InlineKeyboardButton(t('btn_next_item', lang), callback_data=f"portfolio_view_{index + 1}"))
    if nav_row:
        keyboard.append(nav_row)
        
    keyboard.append([
        InlineKeyboardButton(t('btn_edit_caption', lang), callback_data=f"portfolio_edit_cap_{item['id']}"),
        InlineKeyboardButton(t('btn_replace_photo', lang), callback_data=f"portfolio_repl_photo_{item['id']}"),
    ])
    keyboard.append([
        InlineKeyboardButton(t('btn_delete_item', lang), callback_data=f"portfolio_del_{item['id']}")
    ])
    keyboard.append([
        InlineKeyboardButton(t('btn_back_to_portfolio', lang), callback_data="view_portfolio")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    chat_id = None
    if hasattr(query_or_msg, 'message') and query_or_msg.message:
        chat_id = query_or_msg.message.chat_id
        try:
            await query_or_msg.message.delete()
        except Exception:
            pass
    elif hasattr(query_or_msg, 'chat_id'):
        chat_id = query_or_msg.chat_id
    else:
        chat_id = user_id
            
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=item['file_id'],
        caption=card_caption,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return STATE_MAIN_MENU

async def portfolio_add_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    if update.message.photo:
        photo = update.message.photo[-1]
        context.user_data['temp_portfolio_file_id'] = photo.file_id
        
        # Agar rasm bilan birga caption yozilgan bo'lsa
        if update.message.caption:
            caption_text = update.message.caption.strip()
            user_id = update.effective_user.id
            ok, res = await save_user_portfolio_item(user_id, photo.file_id, caption_text)
            if ok:
                await update.message.reply_text(t('photo_uploaded_success', lang, count=res))
            else:
                await update.message.reply_text(t('portfolio_full', lang))
            return await show_portfolio_menu(update.message, context)
            
        await update.message.reply_text(t('prompt_upload_portfolio_caption', lang), parse_mode='HTML')
        return STATE_PORTFOLIO_ADD_CAPTION
    else:
        await update.message.reply_text(t('prompt_upload_portfolio_photo', lang), parse_mode='HTML')
        return STATE_PORTFOLIO_ADD_PHOTO

async def portfolio_add_caption_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption_text = update.message.text.strip() if update.message.text else ""
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    file_id = context.user_data.get('temp_portfolio_file_id')
    
    if file_id:
        ok, res = await save_user_portfolio_item(user_id, file_id, caption_text)
        context.user_data.pop('temp_portfolio_file_id', None)
        if ok:
            await update.message.reply_text(t('photo_uploaded_success', lang, count=res))
        else:
            await update.message.reply_text(t('portfolio_full', lang))
            
    return await show_portfolio_menu(update.message, context)

async def portfolio_edit_caption_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_caption = update.message.text.strip() if update.message.text else ""
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    photo_id = context.user_data.get('target_portfolio_id')
    
    if photo_id:
        await update_portfolio_caption(photo_id, user_id, new_caption)
        await update.message.reply_text(t('caption_updated_success', lang))
        context.user_data.pop('target_portfolio_id', None)
        
    return await show_portfolio_card(update.message, context, context.user_data.get('portfolio_view_index', 0))

async def portfolio_replace_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    photo_id = context.user_data.get('target_portfolio_id')
    
    if update.message.photo and photo_id:
        photo = update.message.photo[-1]
        await replace_portfolio_photo(photo_id, user_id, photo.file_id)
        await update.message.reply_text(t('photo_replaced_success', lang))
        context.user_data.pop('target_portfolio_id', None)
        return await show_portfolio_card(update.message, context, context.user_data.get('portfolio_view_index', 0))
    else:
        await update.message.reply_text(t('prompt_replace_photo', lang), parse_mode='HTML')
        return STATE_PORTFOLIO_REPLACE_PHOTO

# ==================== 3. BANDLIK HOLATI (STATUS) ====================

async def show_status_page(query, context: ContextTypes.DEFAULT_TYPE, change_to: bool = None):
    user_id = query.from_user.id
    lang = context.user_data.get('lang', 'uz')
    
    if change_to is not None:
        is_busy = await set_user_busy_status(user_id, change_to)
    else:
        profile = await get_user_profile(user_id)
        is_busy = profile['is_busy'] if profile else False
        
    if is_busy:
        text = t('status_busy_msg', lang)
        btn_toggle = InlineKeyboardButton(t('btn_set_active', lang), callback_data="status_set_active")
    else:
        text = t('status_active_msg', lang)
        btn_toggle = InlineKeyboardButton(t('btn_set_busy', lang), callback_data="status_set_busy")
        
    keyboard = [
        [btn_toggle],
        [InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")]
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

# ==================== 4. REYTING VA SHARHLAR ====================

async def show_reviews_section(query, context: ContextTypes.DEFAULT_TYPE, page: int = 1):
    user_id = query.from_user.id
    lang = context.user_data.get('lang', 'uz')
    reviews, cur_page, total_pages, rating, completed = await get_user_reviews(user_id, page=page)
    
    header = t(
        'reviews_title',
        lang,
        rating=rating,
        reviews_count=len(reviews),
        completed_count=completed
    ) + "\n\n"
    
    if not reviews:
        content = t('reviews_empty', lang)
    else:
        content = ""
        for r in reviews:
            content += t('review_item', lang, client_name=r['client_name'], rating=r['rating'], comment=r['comment'], date=r['date']) + "───────────────\n"
            
    nav_row = []
    if cur_page > 1:
        nav_row.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"revpage_{cur_page - 1}"))
    if cur_page < total_pages:
        nav_row.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"revpage_{cur_page + 1}"))
        
    keyboard = []
    if nav_row:
        keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")])
    
    await query.message.edit_text(header + content, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

# ==================== 5. SOZLAMALAR ====================

async def show_settings_menu(query, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    keyboard = [
        [InlineKeyboardButton(t('btn_settings_lang', lang), callback_data="settings_lang")],
        [InlineKeyboardButton(t('btn_settings_notif', lang), callback_data="settings_notif")],
        [InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")],
    ]
    await query.message.edit_text(t('settings_title', lang), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

async def show_notifications_settings(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id
    profile = await get_user_profile(user_id)
    lang = context.user_data.get('lang', 'uz')
    
    current_mode = profile.get('notification_setting', 'all')
    mode_titles = {
        'all': t('notif_opt_all', lang),
        'night_mute': t('notif_opt_night', lang),
        'off': t('notif_opt_off', lang),
    }
    
    keyboard = [
        [InlineKeyboardButton(t('notif_opt_all', lang), callback_data="setnotif_all")],
        [InlineKeyboardButton(t('notif_opt_night', lang), callback_data="setnotif_night_mute")],
        [InlineKeyboardButton(t('notif_opt_off', lang), callback_data="setnotif_off")],
        [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_settings")],
    ]
    text = t('notif_title', lang, current=mode_titles.get(current_mode, 'Barchasi yoqiq'))
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

# ==================== 6. QO'LLAB-QUVVATLASH ====================

async def show_support_menu(query, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    settings_info = await get_bot_settings_info()
    
    keyboard = [
        [InlineKeyboardButton(t('btn_guide', lang), callback_data="support_guide")],
        [InlineKeyboardButton(t('btn_write_admin', lang), url="https://t.me/fullxizmat_admin")],
        [InlineKeyboardButton(t('btn_leave_feedback', lang), callback_data="support_feedback")],
        [InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")],
    ]
    text = t('support_title', lang, phone=settings_info['call_center_phone'])
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

async def show_support_guide(query, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'uz')
    keyboard = [
        [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_support")],
        [InlineKeyboardButton(t('btn_back_main', lang), callback_data="back_main")],
    ]
    guide_content = t('guide_text', lang)
    await query.message.edit_text(guide_content, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_MAIN_MENU

async def feedback_text_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    
    await create_user_feedback(user_id, text)
    await update.message.reply_text(t('feedback_received', lang))
    return await show_main_menu(update, context)

# ==================== ISHGA SO'ROV (PROPOSAL) HANDLERS ====================

async def apply_proposal_msg_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message and update.message.text else ""
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    
    target_job = context.user_data.get('apply_target_job')
    if not target_job:
        await update.message.reply_text("Xatolik: E'lon topilmadi.")
        return await show_main_menu(update, context)
        
    context.user_data['temp_proposal_msg'] = text
    
    confirm_text = t(
        'apply_confirm_title',
        lang,
        job_id=target_job['id'],
        title=target_job['title'],
        msg=text
    )
    keyboard = [
        [InlineKeyboardButton(t('btn_send_proposal', lang), callback_data="confirm_apply_send")],
        [
            InlineKeyboardButton(t('btn_edit_proposal', lang), callback_data="edit_apply_msg"),
            InlineKeyboardButton(t('btn_cancel_proposal', lang), callback_data="cancel_apply_proposal")
        ]
    ]
    await update.message.reply_text(confirm_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return STATE_APPLY_PROPOSAL_CONFIRM

async def apply_proposal_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    lang = context.user_data.get('lang', 'uz')
    target_job = context.user_data.get('apply_target_job')
    proposal_msg = context.user_data.get('temp_proposal_msg', '')
    
    if data == "edit_apply_msg":
        if not target_job:
            return await show_main_menu(update, context)
        prompt_text = t(
            'prompt_apply_message',
            lang,
            job_id=target_job['id'],
            title=target_job['title']
        )
        keyboard = [
            [InlineKeyboardButton(t('btn_cancel_proposal', lang), callback_data="cancel_apply_proposal")]
        ]
        await query.message.edit_text(prompt_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return STATE_APPLY_PROPOSAL_MSG
        
    if data == "cancel_apply_proposal":
        context.user_data.pop('apply_target_job', None)
        context.user_data.pop('temp_proposal_msg', None)
        await query.message.delete()
        idx = context.user_data.get('job_index', 0)
        return await show_job_card(query, context, idx)
        
    if data == "confirm_apply_send":
        if not target_job:
            return await show_main_menu(update, context)
            
        ok, res_msg, notif_payload = await create_job_application_in_db(
            target_job['raw_id'],
            target_job['type'],
            user_id,
            proposal_msg
        )
        
        context.user_data.pop('apply_target_job', None)
        context.user_data.pop('temp_proposal_msg', None)
        
        if ok:
            # Agar ish beruvchi telegram ID si mavjud bo'lsa -> Ish beruvchiga bildirishnoma yuborish
            if notif_payload and notif_payload.get('employer_tg_id'):
                await send_employer_notification_about_proposal(notif_payload)
                
            success_text = t('apply_success_msg', lang)
            keyboard = [
                [InlineKeyboardButton(t('btn_menu_jobs', lang), callback_data="menu_jobs")],
                [InlineKeyboardButton(t('btn_goto_main_menu', lang), callback_data="back_main")]
            ]
            await query.message.edit_text(success_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
            return STATE_MAIN_MENU
        else:
            await query.answer(res_msg, show_alert=True)
            await query.message.delete()
            idx = context.user_data.get('job_index', 0)
            return await show_job_card(query, context, idx)

async def send_employer_notification_about_proposal(payload: dict):
    """Ish beruvchiga (Client Bot orqali) usta so'rovi tushganligi haqida bildirishnoma jo'natish"""
    try:
        config = await sync_to_async(BotConfig.get_config)()
        client_bot_token = (config.client_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')).strip()
        if not client_bot_token:
            return
            
        client_bot = Bot(token=client_bot_token)
        employer_tg = payload['employer_tg_id']
        
        notif_msg = (
            f"📬 <b>SIZNING E'LONINGIZGA YANGI JAVOB (ОТКЛИК) TUSHDI!</b>\n\n"
            f"📢 <b>E'lon:</b> #{payload['job_id']} — {payload['job_title']}\n"
            f"👤 <b>Usta:</b> {payload['worker_name']}\n"
            f"✉️ <b>Usta xabari:</b>\n<i>\"{payload['proposal_msg']}\"</i>\n\n"
            f"<i>Ushbu usta bilan tanishish, portfoliosini ko'rish va ishga qabul qilish uchun quyidagi tugmani bosing:</i>"
        )
        keyboard = [
            [InlineKeyboardButton("👥 Javoblarni ko'rish", callback_data=f"view_post_apps_{payload['job_id']}")]
        ]
        await client_bot.send_message(chat_id=employer_tg, text=notif_msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    except Exception as e:
        logger.error(f"Failed to notify employer {payload.get('employer_tg_id')}: {e}")

# ==================== ASOSIY MENYU CALLBACK ROUTER ====================

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    lang = context.user_data.get('lang', 'uz')
    
    # 0. Asosiy menyuga qaytish
    if data == "back_main":
        try:
            await query.answer()
        except Exception:
            pass
        return await show_main_menu(update, context)
        
    # 1. Ishlarni ko'rish / qidirish
    if data == "menu_jobs":
        try:
            await query.answer()
        except Exception:
            pass
        return await show_jobs_sub_menu(query, context)
        
    if data == "jobs_matched":
        try:
            await query.answer()
        except Exception:
            pass
        context.user_data['last_feed_filter'] = {'filter_type': 'matched'}
        jobs = await fetch_jobs_feed(user_id, filter_type='matched')
        context.user_data['current_jobs_list'] = jobs
        return await show_job_card(query, context, 0)
        
    if data == "jobs_by_cat":
        try:
            await query.answer()
        except Exception:
            pass
        categories, _, _ = await get_categories_page(lang=lang, page=1)
        keyboard = []
        for cat_id, cat_name in categories:
            keyboard.append([InlineKeyboardButton(cat_name, callback_data=f"feedcat_{cat_id}")])
        keyboard.append([InlineKeyboardButton(t('btn_back', lang), callback_data="menu_jobs")])
        try:
            await query.message.edit_text(t('jobs_menu_title', lang), reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception as e:
            if "Message is not modified" not in str(e):
                logger.error(f"Error in jobs_by_cat edit_text: {e}")
        return STATE_MAIN_MENU
        
    if data.startswith("feedcat_"):
        try:
            await query.answer()
        except Exception:
            pass
        cat_id = int(data.replace("feedcat_", ""))
        context.user_data['last_feed_filter'] = {'filter_type': 'category', 'cat_id': cat_id}
        jobs = await fetch_jobs_feed(user_id, filter_type='category', cat_id=cat_id)
        context.user_data['current_jobs_list'] = jobs
        return await show_job_card(query, context, 0)
        
    if data == "jobs_by_geo":
        try:
            await query.answer()
        except Exception:
            pass
        keyboard = [
            [InlineKeyboardButton(t('btn_geo_district', lang), callback_data="feedgeo_district")],
            [InlineKeyboardButton(t('btn_geo_region', lang), callback_data="feedgeo_region")],
            [
                InlineKeyboardButton(t('btn_geo_radius_5', lang), callback_data="feedgeo_r5"),
                InlineKeyboardButton(t('btn_geo_radius_10', lang), callback_data="feedgeo_r10"),
            ],
            [
                InlineKeyboardButton(t('btn_geo_radius_25', lang), callback_data="feedgeo_r25"),
            ],
            [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_jobs")],
        ]
        try:
            await query.message.edit_text(t('jobs_menu_title', lang), reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception as e:
            if "Message is not modified" not in str(e):
                logger.error(f"Error in jobs_by_geo edit_text: {e}")
        return STATE_MAIN_MENU
        
    if data.startswith("feedgeo_"):
        try:
            await query.answer()
        except Exception:
            pass
        geo_type = data.replace("feedgeo_", "")
        if geo_type == 'r5':
            filt = {'filter_type': 'radius', 'radius': 5}
        elif geo_type == 'r10':
            filt = {'filter_type': 'radius', 'radius': 10}
        elif geo_type == 'r25':
            filt = {'filter_type': 'radius', 'radius': 25}
        elif geo_type == 'district':
            filt = {'filter_type': 'district'}
        else:
            filt = {'filter_type': 'region'}
            
        context.user_data['last_feed_filter'] = filt
        jobs = await fetch_jobs_feed(user_id, **filt)
        context.user_data['current_jobs_list'] = jobs
        return await show_job_card(query, context, 0)
        
    if data.startswith("job_nav_"):
        try:
            await query.answer()
        except Exception:
            pass
        idx = int(data.replace("job_nav_", ""))
        return await show_job_card(query, context, idx)
        
    if data == "job_refresh":
        filt = context.user_data.get('last_feed_filter', {'filter_type': 'matched'})
        jobs = await fetch_jobs_feed(user_id, **filt)
        context.user_data['current_jobs_list'] = jobs
        idx = context.user_data.get('job_index', 0)
        try:
            await query.answer("🔄 Ishlar ro'yxati yangilandi!")
        except Exception:
            pass
        return await show_job_card(query, context, idx)
        
    if data.startswith("job_check_"):
        job_id_str = data.replace("job_check_", "")
        jobs = context.user_data.get('current_jobs_list', [])
        idx = context.user_data.get('job_index', 0)
        
        target_job = None
        if jobs and 0 <= idx < len(jobs) and jobs[idx]['id'] == job_id_str:
            target_job = jobs[idx]
        else:
            for j in jobs:
                if j['id'] == job_id_str:
                    target_job = j
                    break
                    
        if not target_job:
            target_job = await fetch_single_job(job_id_str, lang=lang)

        if not target_job:
            try:
                await query.answer(t('job_status_closed_alert', lang), show_alert=True)
            except Exception:
                pass
            return STATE_MAIN_MENU
            
        check_res = await check_job_status_in_db(target_job['raw_id'], target_job['type'], user_id)
        try:
            if check_res['status'] == 'ACTIVE':
                if check_res['already_applied']:
                    await query.answer(t('job_already_applied_alert', lang), show_alert=True)
                else:
                    await query.answer(t('job_status_active_alert', lang), show_alert=True)
            elif check_res['status'] == 'TAKEN':
                await query.answer(t('job_status_taken_alert', lang), show_alert=True)
            else:
                await query.answer(t('job_status_closed_alert', lang), show_alert=True)
        except Exception as e:
            logger.error(f"Error answering job_check query: {e}")
        return STATE_MAIN_MENU

    # 1.3. GPS Joylashuvni yangilash
    if data == "menu_update_gps":
        try:
            await query.answer()
        except Exception:
            pass
        keyboard = [
            [KeyboardButton(t('btn_send_gps', lang), request_location=True)],
            [KeyboardButton(t('btn_cancel', lang))]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        try:
            await query.message.delete()
        except Exception:
            pass
        await query.message.chat.send_message(t('prompt_send_gps_update', lang), reply_markup=reply_markup, parse_mode='HTML')
        return STATE_UPDATE_LOCATION

    # 1.4. To'g'ridan-to'g'ri ishni ko'rish (Push-bildirishnomadan kelganda)
    if data.startswith("view_job_"):
        job_raw_id = int(data.replace("view_job_", ""))
        single_job = await fetch_single_job_post(job_raw_id, lang=lang)
        if not single_job:
            await query.answer("Ushbu e'lon topilmadi yoki o'chirilgan.", show_alert=True)
            return STATE_MAIN_MENU
        context.user_data['current_jobs_list'] = [single_job]
        context.user_data['job_index'] = 0
        return await show_job_card(query, context, 0)

    if data.startswith("job_take_"):
        try:
            await query.answer()
        except Exception:
            pass

        job_id_str = data.replace("job_take_", "")
        jobs = context.user_data.get('current_jobs_list', [])
        idx = context.user_data.get('job_index', 0)
        
        target_job = None
        if jobs and 0 <= idx < len(jobs) and jobs[idx]['id'] == job_id_str:
            target_job = jobs[idx]
        else:
            for j in jobs:
                if j['id'] == job_id_str:
                    target_job = j
                    break
                    
        if not target_job:
            target_job = await fetch_single_job(job_id_str, lang=lang)

        if not target_job:
            try:
                await query.answer(t('job_status_closed_alert', lang), show_alert=True)
            except Exception:
                pass
            return STATE_MAIN_MENU
            
        # Check active status first
        check_res = await check_job_status_in_db(target_job['raw_id'], target_job['type'], user_id)
        if check_res['status'] == 'TAKEN':
            try:
                await query.answer(t('job_status_taken_alert', lang), show_alert=True)
            except Exception:
                pass
            return STATE_MAIN_MENU
        elif check_res['status'] == 'CLOSED':
            try:
                await query.answer(t('job_status_closed_alert', lang), show_alert=True)
            except Exception:
                pass
            return STATE_MAIN_MENU
            
        # Save applying target job in context
        context.user_data['apply_target_job'] = target_job
        
        prompt_text = t(
            'prompt_apply_message',
            lang,
            job_id=target_job['id'],
            title=target_job['title']
        )
        keyboard = [
            [InlineKeyboardButton(t('btn_cancel_proposal', lang), callback_data="cancel_apply_proposal")]
        ]
        try:
            await query.message.edit_text(prompt_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        except Exception:
            await query.message.reply_text(prompt_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return STATE_APPLY_PROPOSAL_MSG
        
    if data.startswith("contact_job_"):
        jobs = context.user_data.get('current_jobs_list', [])
        job_idx = context.user_data.get('job_index', 0)
        contact_info = "Aloqa raqami mavjud emas"
        if jobs and 0 <= job_idx < len(jobs):
            target = jobs[job_idx]
            contact_info = f"👤 {target.get('customer_name')}\n📞 Tel: {target.get('contact')}"
        await query.answer(text=contact_info, show_alert=True)
        return STATE_MAIN_MENU
        
    # 1.5. Javoblar (Yuborilgan so'rovlar)
    if data == "menu_my_applications":
        return await worker_applications_menu_handler(update, context, page=0)
        
    if data.startswith("my_app_page_"):
        page_num = int(data.replace("my_app_page_", ""))
        return await worker_applications_menu_handler(update, context, page=page_num)
        
    if data.startswith("my_app_view_"):
        app_id_val = int(data.replace("my_app_view_", ""))
        return await worker_application_detail_handler(update, context, app_id=app_id_val)

    if data.startswith("my_app_del_"):
        app_id_val = int(data.replace("my_app_del_", ""))
        success = await delete_worker_application_in_db(app_id_val, user_id)
        if success:
            await query.answer(t('app_deleted_success', lang), show_alert=True)
        else:
            await query.answer("So'rov topilmadi!", show_alert=True)
        return await worker_applications_menu_handler(update, context, page=0)

    # 2. Mening profilim (Kabinet)
    if data == "menu_profile":
        return await show_profile_cabinet(query, context)
        
    if data == "edit_profile_menu":
        keyboard = [
            [InlineKeyboardButton(t('btn_edit_name_age', lang), callback_data="edit_name_age")],
            [InlineKeyboardButton(t('btn_edit_phone', lang), callback_data="edit_phone")],
            [InlineKeyboardButton(t('btn_edit_location', lang), callback_data="edit_location")],
            [InlineKeyboardButton(t('btn_edit_positions', lang), callback_data="edit_positions")],
            [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_profile")],
        ]
        await query.message.edit_text(t('edit_menu_title', lang), reply_markup=InlineKeyboardMarkup(keyboard))
        return STATE_MAIN_MENU
        
    if data == "edit_name_age":
        await query.message.reply_text(t('step1_name_title', lang), parse_mode='HTML')
        return STATE_FULL_NAME
        
    if data == "edit_phone":
        keyboard = [[KeyboardButton(t('btn_send_phone', lang), request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await query.message.delete()
        await query.message.chat.send_message(t('step1_phone_title', lang), reply_markup=reply_markup)
        return STATE_PHONE
        
    if data == "edit_location":
        try:
            await query.answer()
        except Exception:
            pass
        keyboard = [
            [KeyboardButton(t('btn_send_gps', lang), request_location=True)],
            [KeyboardButton(t('btn_cancel', lang))]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        try:
            await query.message.delete()
        except Exception:
            pass
        await query.message.chat.send_message(t('step2_geo_title', lang), reply_markup=reply_markup, parse_mode='HTML')
        return STATE_UPDATE_LOCATION
        
    if data == "edit_positions":
        return await show_categories_page(query.message, context, page=1)
        
    # Portfolio
    if data == "view_portfolio":
        return await show_portfolio_menu(query, context)
        
    if data == "portfolio_add":
        await query.message.reply_text(t('prompt_upload_portfolio_photo', lang), parse_mode='HTML')
        return STATE_PORTFOLIO_ADD_PHOTO
        
    if data.startswith("portfolio_view_"):
        idx = int(data.replace("portfolio_view_", ""))
        return await show_portfolio_card(query, context, idx)
        
    if data.startswith("portfolio_edit_cap_"):
        photo_id = int(data.replace("portfolio_edit_cap_", ""))
        context.user_data['target_portfolio_id'] = photo_id
        await query.message.reply_text(t('prompt_edit_caption', lang), parse_mode='HTML')
        return STATE_PORTFOLIO_EDIT_CAPTION
        
    if data.startswith("portfolio_repl_photo_"):
        photo_id = int(data.replace("portfolio_repl_photo_", ""))
        context.user_data['target_portfolio_id'] = photo_id
        await query.message.reply_text(t('prompt_replace_photo', lang), parse_mode='HTML')
        return STATE_PORTFOLIO_REPLACE_PHOTO
        
    if data.startswith("portfolio_del_"):
        photo_id = int(data.replace("portfolio_del_", ""))
        await delete_user_portfolio_photo(photo_id, user_id)
        await query.answer(t('photo_deleted_success', lang), show_alert=True)
        return await show_portfolio_menu(query, context)
        
    # 3. Bandlik holati (Status ko'rish va o'zgartirish)
    if data == "menu_toggle_status":
        return await show_status_page(query, context, change_to=None)
        
    if data == "status_set_active":
        return await show_status_page(query, context, change_to=False)
        
    if data == "status_set_busy":
        return await show_status_page(query, context, change_to=True)
        
    # 4. Reyting va Sharhlar
    if data == "menu_reviews":
        return await show_reviews_section(query, context, page=1)
        
    if data.startswith("revpage_"):
        page = int(data.replace("revpage_", ""))
        return await show_reviews_section(query, context, page=page)
        
    # 5. Sozlamalar
    if data == "menu_settings":
        return await show_settings_menu(query, context)
        
    if data == "settings_lang":
        keyboard = [
            [
                InlineKeyboardButton("🇺🇿 O'zbekcha (Lotin)", callback_data="setlang_uz"),
                InlineKeyboardButton("🇺🇿 Ўзбекча (Крилл)", callback_data="setlang_oz"),
            ],
            [
                InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang_ru"),
                InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en"),
            ],
            [InlineKeyboardButton(t('btn_back', lang), callback_data="menu_settings")]
        ]
        await query.message.edit_text(t('choose_lang', lang), reply_markup=InlineKeyboardMarkup(keyboard))
        return STATE_MAIN_MENU
        
    if data.startswith("setlang_"):
        new_lang = data.replace("setlang_", "")
        await update_user_language(user_id, new_lang)
        context.user_data['lang'] = new_lang
        return await show_main_menu(update, context)
        
    if data == "settings_notif":
        return await show_notifications_settings(query, context)
        
    if data.startswith("setnotif_"):
        mode = data.replace("setnotif_", "")
        await update_user_notification(user_id, mode)
        await query.answer(t('notif_saved', lang), show_alert=True)
        return await show_notifications_settings(query, context)
        
    # 6. Qo'llab-quvvatlash
    if data == "menu_support":
        return await show_support_menu(query, context)
        
    if data == "support_guide":
        return await show_support_guide(query, context)
        
    if data == "support_feedback":
        await query.message.reply_text(t('prompt_feedback', lang))
        return STATE_SEND_FEEDBACK
        
    if data == "reset_to_main_menu":
        return await reset_to_main_menu_callback(update, context)
        
    if data == "noop":
        return STATE_MAIN_MENU
        
    return await unhandled_callback_fallback(update, context)

async def update_location_received_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loc = update.message.location if update.message else None
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'uz')
    
    if loc:
        lat, lon = loc.latitude, loc.longitude
        geo_info = await save_location_from_gps(user_id, lat, lon)
        profile = await get_user_profile(user_id)
        
        success_msg = t('gps_updated_success', lang, region=profile['region'], district=profile['district'], gps=f"{lat:.5f}, {lon:.5f}")
        await update.message.reply_text(success_msg, reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')
        return await show_main_menu(update, context)
    else:
        cancel_text = "❌ Joylashuvni yangilash bekor qilindi."
        if lang == 'oz':
            cancel_text = "❌ Жойлашувни янгилаш бекор қилинди."
        elif lang == 'ru':
            cancel_text = "❌ Обновление локации отменено."
        elif lang == 'en':
            cancel_text = "❌ Location update cancelled."
        await update.message.reply_text(cancel_text, reply_markup=ReplyKeyboardRemove())
        return await show_main_menu(update, context)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Amallar bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def build_bot_application(token: str) -> Application:
    app = ApplicationBuilder().token(token).build()
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_command),
            CommandHandler('menu', show_main_menu),
        ],
        states={
            STATE_LANGUAGE: [
                CallbackQueryHandler(language_callback, pattern="^lang_"),
            ],
            STATE_ROLE: [
                CallbackQueryHandler(role_callback, pattern="^role_"),
                CallbackQueryHandler(language_callback, pattern="^back_to_lang$"),
            ],
            STATE_GENDER: [
                CallbackQueryHandler(gender_callback, pattern="^(gender_|back_to_role)"),
            ],
            STATE_FULL_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, full_name_input_handler),
            ],
            STATE_AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, age_input_handler),
            ],
            STATE_PHONE: [
                MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), phone_input_handler),
            ],
            STATE_GEO_LOCATION: [
                MessageHandler(filters.LOCATION | (filters.TEXT & ~filters.COMMAND), geo_location_handler),
            ],
            STATE_MANUAL_REGION: [
                CallbackQueryHandler(manual_region_callback, pattern="^reg_"),
            ],
            STATE_STREET_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, street_address_input_handler),
            ],
            STATE_CATEGORY: [
                CallbackQueryHandler(category_callback, pattern="^(cat_|catpage_|noop|pos_done)"),
            ],
            STATE_POSITION: [
                CallbackQueryHandler(position_callback, pattern="^(pos_|pospage_|noop|pos_done|back_to_cat_list)"),
            ],
            STATE_EMPLOYMENT_TYPE: [
                CallbackQueryHandler(employment_type_callback, pattern="^emp_"),
            ],
            STATE_WORK_SCHEDULE: [
                CallbackQueryHandler(work_schedule_callback, pattern="^sched_"),
            ],
            STATE_CONFIRM_PROFILE: [
                CallbackQueryHandler(confirm_profile_callback, pattern="^(confirm_save|restart_flow)"),
            ],
            STATE_MAIN_MENU: [
                CallbackQueryHandler(main_menu_callback, pattern=".*"),
            ],
            STATE_UPDATE_LOCATION: [
                MessageHandler(filters.LOCATION | (filters.TEXT & ~filters.COMMAND), update_location_received_handler),
                CommandHandler('menu', show_main_menu),
                CommandHandler('start', start_command),
            ],
            STATE_PORTFOLIO_ADD_PHOTO: [
                MessageHandler(filters.PHOTO, portfolio_add_photo_handler),
                CommandHandler('menu', show_main_menu),
                CommandHandler('start', start_command),
            ],
            STATE_PORTFOLIO_ADD_CAPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, portfolio_add_caption_handler),
                CommandHandler('menu', show_main_menu),
                CommandHandler('start', start_command),
            ],
            STATE_PORTFOLIO_EDIT_CAPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, portfolio_edit_caption_handler),
                CommandHandler('menu', show_main_menu),
                CommandHandler('start', start_command),
            ],
            STATE_PORTFOLIO_REPLACE_PHOTO: [
                MessageHandler(filters.PHOTO, portfolio_replace_photo_handler),
                CommandHandler('menu', show_main_menu),
                CommandHandler('start', start_command),
            ],
            STATE_SEND_FEEDBACK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_text_received),
                CommandHandler('menu', show_main_menu),
                CommandHandler('start', start_command),
            ],
            STATE_APPLY_PROPOSAL_MSG: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, apply_proposal_msg_received),
                CallbackQueryHandler(apply_proposal_confirm_callback, pattern="^(cancel_apply_proposal|edit_apply_msg)"),
                CommandHandler('menu', show_main_menu),
                CommandHandler('start', start_command),
            ],
            STATE_APPLY_PROPOSAL_CONFIRM: [
                CallbackQueryHandler(apply_proposal_confirm_callback, pattern="^(confirm_apply_send|edit_apply_msg|cancel_apply_proposal)"),
                CommandHandler('menu', show_main_menu),
                CommandHandler('start', start_command),
            ]
        },
        fallbacks=[
            CommandHandler('start', start_command),
            CommandHandler('cancel', cancel_command),
            CommandHandler('menu', show_main_menu),
            MessageHandler(filters.LOCATION, update_location_received_handler),
            CallbackQueryHandler(reset_to_main_menu_callback, pattern="^reset_to_main_menu$"),
            CallbackQueryHandler(unhandled_callback_fallback, pattern=".*"),
        ],
        allow_reentry=True,
    )
    
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(reset_to_main_menu_callback, pattern="^reset_to_main_menu$"))
    app.add_handler(CallbackQueryHandler(unhandled_callback_fallback, pattern=".*"))
    app.add_error_handler(global_error_handler)
    return app

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

async def unhandled_callback_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Eski yoki tanilmagan tugmalar bosilganda chiqadigan xushmuomala xabarnoma"""
    query = update.callback_query
    if query:
        await query.answer()
    
    user_id = update.effective_user.id
    db_user = await get_user_db_record(user_id)
    lang = db_user['language'] if db_user else context.user_data.get('lang', 'uz')
    
    text = t('bot_outdated_button_msg', lang)
    if query and query.message:
        try:
            await query.edit_message_text(text, reply_markup=None, parse_mode='HTML')
        except Exception:
            await query.message.reply_text(text, reply_markup=None, parse_mode='HTML')
    elif update.effective_message:
        await update.effective_message.reply_text(text, reply_markup=None, parse_mode='HTML')
    return STATE_MAIN_MENU

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception while handling an update in worker bot: {context.error}", exc_info=context.error)
    try:
        lang = 'uz'
        if context.user_data and 'lang' in context.user_data:
            lang = context.user_data['lang']
        elif isinstance(update, Update) and update.effective_user:
            db_user = await get_user_db_record(update.effective_user.id)
            if db_user and db_user.get('language'):
                lang = db_user['language']
            
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
        logger.error(f"Failed to send error message to worker user: {e}")

def main():
    config = BotConfig.get_config()
    token = config.client_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    print("=== 24/7-ISHLAR TELEGRAM BOT ISHGA TUSHMOQDA ===")
    app = build_bot_application(token)
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
