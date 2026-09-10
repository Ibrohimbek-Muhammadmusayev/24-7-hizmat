import logging
import asyncio
from datetime import datetime
from asgiref.sync import sync_to_async

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from django.conf import settings
from accounts.models import User
from categories.models import Category
from orders.models import Order
from locations.models import WorkerLocation
from bot_control.models import BotConfig

logger = logging.getLogger(__name__)

# --- CONVERSATION STATES ---
(
    WORKER_REGISTER_NAME,
    WORKER_REGISTER_PHONE,
    WORKER_REGISTER_CAT,
    WORKER_EDIT_NAME,
    WORKER_EDIT_PHONE,
    WORKER_UPDATE_LOC,
) = range(6)

# --- KEYBOARDS ---

def get_worker_keyboard(user=None):
    is_online = getattr(user, 'is_online', False) if user else False
    status_btn = "🔴 Offline Bo'lish" if is_online else "🟢 Online Bo'lish"
    
    row1 = [KeyboardButton("🔍 Yangi Ishlarni Qidirish"), KeyboardButton("📋 Mening Ishlarim")]
    row2 = [KeyboardButton(status_btn), KeyboardButton("👤 Usta Profili")]
    row3 = [KeyboardButton("📍 GPS Yangilash"), KeyboardButton("📞 Call Center")]
    return ReplyKeyboardMarkup([row1, row2, row3], resize_keyboard=True)

import math

def calculate_distance_km(lat1, lon1, lat2, lon2):
    try:
        if not lat1 or not lon1 or not lat2 or not lon2:
            return None
        R = 6371.0 # Earth radius in km
        dlat = math.radians(float(lat2) - float(lat1))
        dlon = math.radians(float(lon2) - float(lon1))
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 1)
    except Exception:
        return None

# --- DB HELPERS ---

@sync_to_async
def get_bot_config():
    return BotConfig.get_config()

@sync_to_async
def get_or_create_worker_user(tg_user):
    user = User.objects.select_related('category').filter(telegram_id=tg_user.id).first()
    if not user:
        user = User.objects.create(
            telegram_id=tg_user.id,
            username=f"tg_w_{tg_user.id}",
            first_name=tg_user.first_name or '',
            last_name=tg_user.last_name or '',
            role=User.Role.WORKER,
            is_online=True,
            started_worker_bot=True,
        )
    else:
        changed = False
        if not user.started_worker_bot:
            user.started_worker_bot = True
            changed = True
        if user.role != User.Role.ADMIN and user.role != User.Role.CALL_CENTER and user.role != User.Role.WORKER:
            user.role = User.Role.WORKER
            changed = True
        if changed:
            user.save()
    return user

@sync_to_async
def get_active_categories():
    return list(Category.objects.filter(is_active=True))

@sync_to_async
def get_categories_with_job_counts():
    cats = list(Category.objects.filter(is_active=True))
    result = []
    for cat in cats:
        cnt = Order.objects.filter(status=Order.Status.PENDING, category=cat).count()
        result.append((cat, cnt))
    return result

@sync_to_async
def get_category_by_id(cat_id):
    return Category.objects.filter(id=cat_id).first()

@sync_to_async
def set_worker_category(tg_id, cat_id):
    user = User.objects.select_related('category').filter(telegram_id=tg_id).first()
    category = Category.objects.filter(id=cat_id).first()
    if user and category:
        user.category = category
        user.specialty = category.name
        user.save()
        return user, category
    return None, None

@sync_to_async
def toggle_worker_online(tg_id):
    user = User.objects.filter(telegram_id=tg_id).first()
    if user:
        user.is_online = not user.is_online
        user.save()
        return user.is_online
    return False

@sync_to_async
def update_worker_location_db(tg_id, lat, lng):
    user = User.objects.filter(telegram_id=tg_id).first()
    if user:
        loc, created = WorkerLocation.objects.get_or_create(
            worker=user,
            defaults={'latitude': lat, 'longitude': lng, 'heading': 0.0}
        )
        if not created:
            loc.latitude = lat
            loc.longitude = lng
            loc.save()
        return True
    return False

@sync_to_async
def get_available_jobs_for_worker(tg_id, filter_mode='MATCHED', cat_id=None):
    user = User.objects.select_related('category').filter(telegram_id=tg_id).first()
    qs = Order.objects.select_related('category', 'assigned_worker').filter(status=Order.Status.PENDING)

    worker_loc = WorkerLocation.objects.filter(worker=user).first() if user else None
    w_lat = worker_loc.latitude if worker_loc else None
    w_lng = worker_loc.longitude if worker_loc else None

    target_category = None
    if filter_mode == 'MATCHED':
        if user and user.category:
            target_category = user.category
            qs = qs.filter(category=user.category)
        else:
            filter_mode = 'ALL'

    elif filter_mode == 'CATEGORY' and cat_id:
        target_category = Category.objects.filter(id=cat_id).first()
        if target_category:
            qs = qs.filter(category=target_category)

    orders_list = list(qs.order_by('-created_at')[:40])

    # Attach distance
    results = []
    for order in orders_list:
        dist = None
        if w_lat and w_lng and order.latitude and order.longitude:
            dist = calculate_distance_km(w_lat, w_lng, order.latitude, order.longitude)
        results.append((order, dist))

    if filter_mode == 'NEARBY':
        # Sort by distance (putting items with distance first)
        results.sort(key=lambda x: (x[1] is None, x[1] if x[1] is not None else 99999))
        results = results[:10]
    else:
        results = results[:8]

    has_location = bool(w_lat and w_lng)
    return results, target_category, has_location

@sync_to_async
def get_worker_my_jobs(tg_id, filter_type='ACTIVE'):
    user = User.objects.filter(telegram_id=tg_id).first()
    if not user:
        return []
    qs = Order.objects.select_related('category', 'assigned_worker').filter(assigned_worker=user)
    if filter_type == 'ACTIVE':
        qs = qs.filter(status__in=[Order.Status.DISPATCHED, Order.Status.STARTED])
    elif filter_type == 'FINISHED':
        qs = qs.filter(status=Order.Status.FINISHED)
    return list(qs.order_by('-created_at')[:10])

@sync_to_async
def accept_job_by_worker(tg_id, order_id):
    user = User.objects.filter(telegram_id=tg_id).first()
    if not user:
        return False, "Foydalanuvchi topilmadi"
    order = Order.objects.filter(id=order_id).first()
    if not order:
        return False, "Buyurtma topilmadi"
    if order.status != Order.Status.PENDING:
        return False, f"Ushbu buyurtma allaqachon boshqa usta tomonidan qabul qilingan yoki yakunlangan (Holati: {order.status})"
    
    order.assigned_worker = user
    order.status = Order.Status.DISPATCHED
    order.save()
    return True, order

@sync_to_async
def finish_job_by_worker(tg_id, order_id):
    user = User.objects.filter(telegram_id=tg_id).first()
    if not user:
        return False, "Foydalanuvchi topilmadi"
    order = Order.objects.filter(id=order_id, assigned_worker=user).first()
    if not order:
        return False, "Ushbu buyurtma sizga biriktirilmagan yoki topilmadi"
    
    order.status = Order.Status.FINISHED
    order.save()
    return True, order

@sync_to_async
def check_order_status_db(order_id):
    return Order.objects.filter(id=order_id).first()

@sync_to_async
def update_worker_name(tg_id, new_name):
    user = User.objects.filter(telegram_id=tg_id).first()
    if user:
        user.first_name = new_name
        user.save()
        return user
    return None

@sync_to_async
def update_worker_phone(tg_id, phone):
    user = User.objects.filter(telegram_id=tg_id).first()
    if user:
        user.phone_number = phone
        user.save()
        return user
    return None

# --- COMMAND HANDLERS ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_worker_user(update.effective_user)
    config = await get_bot_config()
    kb = get_worker_keyboard(user)

    first_name = update.effective_user.first_name or user.first_name or "Usta"

    cat_str = f"🛠️ Mutaxassislik: <b>{user.category.name}</b>\n" if user.category else "⚠️ <i>Mutaxassisligingiz belgilanmagan. Pastdagi menyudan Profil orqali sohangizni tanlang.</i>\n"

    welcome_text = (
        f"Assalomu alaykum, <b>{first_name}</b>! 👋\n\n"
        "<b>Full-Xizmat (Ishchilar va Ustalar Boti)</b>ga xush kelibsiz!\n\n"
        f"{cat_str}"
        "Ushbu bot orqali siz real vaqt rejimida yangi buyurtmalarni qabul qilishingiz va daromad topishingiz mumkin.\n\n"
        "Kerakli bo'limni tanlang:"
    )

    if not user.category:
        categories = await get_active_categories()
        buttons = []
        for cat in categories:
            buttons.append([InlineKeyboardButton(f"{cat.icon} {cat.name}", callback_data=f"w_reg_cat_{cat.id}")])
        inline_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_html(
            f"Assalomu alaykum, <b>{first_name}</b>! 👋\n\n"
            "Ishlarni qabul qilish uchun iltimos, <b>asosiy mutaxassislik yo'nalishingizni tanlang:</b>",
            reply_markup=inline_markup
        )
        return

    await update.message.reply_html(welcome_text, reply_markup=kb)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = await get_bot_config()
    phone = config.call_center_phone or "+998 (71) 200-00-00"

    text = (
        "<b>ℹ️ USTALAR UCHUN YORDAM & CALL CENTER</b>\n\n"
        "• <b>Yangi Ishlarni Qidirish:</b> Bo'sh buyurtmalarni ko'rish va qabul qilish.\n"
        "• <b>Mening Ishlarim:</b> Olingan buyurtmalar va mijoz kontaktlari.\n"
        "• <b>Online / Offline:</b> Yangi ishlar kelishi uchun holatingizni yoqing.\n"
        "• <b>GPS Yangilash:</b> Xaritada mijozlarga yaqin ko'rinish uchun joylashuvni yangilang.\n\n"
        f"📞 <b>Dispetcher / Operator:</b> <code>{phone}</code>"
    )

    inline_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"📞 Qo'ng'iroq Qilish ({phone})", url=f"https://t.me/share/url?url=Tel:{phone}")],
        [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
    ])

    if update.message:
        await update.message.reply_html(text, reply_markup=inline_kb)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=inline_kb)

# --- WORKER REGISTRATION / CATEGORY PICKER ---

async def worker_reg_cat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat_id = int(query.data.split('_')[3])

    user, cat = await set_worker_category(query.from_user.id, cat_id)
    kb = get_worker_keyboard(user)

    await query.edit_message_text(
        f"✅ <b>Mutaxassisligingiz muvaffaqiyatli saqlandi:</b> {cat.name} {cat.icon}\n\n"
        "Endi siz ushbu sohadagi barcha yangi buyurtmalarni qabul qilishingiz mumkin.",
        parse_mode='HTML'
    )
    await query.message.reply_text("Bosh menyu:", reply_markup=kb)

# --- ISH QIDIRISH (MULTI-FILTER INTERACTIVE FEED) ---

async def search_jobs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Default entry point: Show matched jobs for worker's category
    return await render_worker_jobs_feed(update, context, filter_mode='MATCHED')

async def render_worker_jobs_feed(update: Update, context: ContextTypes.DEFAULT_TYPE, filter_mode='MATCHED', cat_id=None):
    user_id = update.effective_user.id if update.effective_user else update.callback_query.from_user.id
    user = await get_or_create_worker_user(update.effective_user if update.effective_user else update.callback_query.from_user)

    orders_with_dist, category, has_location = await get_available_jobs_for_worker(user_id, filter_mode=filter_mode, cat_id=cat_id)

    # Title header text depending on filter mode
    if filter_mode == 'MATCHED':
        cat_title = category.name if category else 'Sizning Sohangiz'
        title_header = f"🎯 <b>SIZGA TAVSIYA QILINGAN ISHLAR ({cat_title})</b>"
        empty_hint = f"Sizning sohangizda (<b>{cat_title}</b>) hozircha yangi bo'sh ishlar mavjud emas."
    elif filter_mode == 'NEARBY':
        title_header = "📍 <b>SIZGA ENG YAQIN ATROFDAGI ISHLAR</b>"
        empty_hint = "Hozirda yaqin masofadagi bo'sh ishlar topilmadi."
    elif filter_mode == 'CATEGORY':
        cat_title = category.name if category else 'Tanlangan Soha'
        title_header = f"📂 <b>{cat_title.upper()} SOHASIDAGI ISHLAR</b>"
        empty_hint = f"<b>{cat_title}</b> sohasida hozircha yangi ishlar mavjud emas."
    else:
        title_header = "🌐 <b>BARCHA MAVJUD BO'SH ISHLAR</b>"
        empty_hint = "Hozirda platformada bo'sh ishlar mavjud emas."

    # Top Filter Buttons (Qisqa va Tushunarli)
    filter_buttons = [
        [
            InlineKeyboardButton("🎯 Menga Mos", callback_data="w_filter_matched"),
            InlineKeyboardButton("📍 Yaqin Atrof", callback_data="w_filter_nearby")
        ],
        [
            InlineKeyboardButton("🌐 Barcha Ishlar", callback_data="w_filter_all"),
            InlineKeyboardButton("📂 Boshqa Soha", callback_data="w_filter_cats")
        ]
    ]

    # If no orders found
    if not orders_with_dist:
        location_tip = ""
        if filter_mode == 'NEARBY' and not has_location:
            location_tip = "\n\n💡 <i>Yaqin atrofdagi ishlarni ko'rish uchun avval menyudan <b>«📍 GPS Yangilash»</b> tugmasini bosing.</i>"

        text = (
            f"{title_header}\n\n"
            f"🔍 {empty_hint}{location_tip}\n\n"
            "<i>Quyidagi bo'limlardan boshqa ishlarni ko'rishingiz mumkin:</i>"
        )
        empty_markup = InlineKeyboardMarkup(filter_buttons + [
            [InlineKeyboardButton("🔄 Qayta Tekshirish", callback_data=f"w_filter_{filter_mode.lower()}")],
            [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
        ])

        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=empty_markup)
        else:
            await update.message.reply_html(text, reply_markup=empty_markup)
        return

    # If orders exist, show header then each order card
    header_msg = f"{title_header} (Jami: <b>{len(orders_with_dist)} ta</b>):\n<i>Kerakli ishni tanlab <b>«Qabul Qilish»</b>ni bosing:</i>"
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(header_msg, parse_mode='HTML')
        target_msg = update.callback_query.message
    else:
        await update.message.reply_html(header_msg)
        target_msg = update.message

    format_map = {'OFFLINE': '📍 Joyida (Offline)', 'ONLINE': '💻 Masofaviy (Online)'}

    for order, dist in orders_with_dist:
        fmt_label = format_map.get(order.work_format, '📍 Joyida')
        created_str = order.created_at.strftime("%H:%M, %d.%m.%Y") if hasattr(order, 'created_at') and order.created_at else ''
        dist_str = f" (🚗 ~{dist} km)" if dist is not None else ""

        card_text = (
            f"<b>🆔 ISH RAQAMI: #{order.id}</b>\n"
            f"📌 <b>Nom:</b> {order.title}\n"
            f"📁 <b>Soha:</b> {order.service_type}\n"
            f"🌐 <b>Format:</b> {fmt_label}\n"
            f"📍 <b>Manzil:</b> {order.address}{dist_str}\n"
            f"💰 <b>Narx:</b> <b>{order.price:,.0f} SUM</b>\n"
            f"📄 <b>Tavsif:</b> {order.description}\n"
            f"📅 <b>Vaqt:</b> {created_str}\n"
        )

        card_buttons = [
            [
                InlineKeyboardButton("✅ Ishni Qabul Qilish", callback_data=f"accept_job_{order.id}"),
                InlineKeyboardButton("🔄 Holatni Tekshirish", callback_data=f"check_job_{order.id}")
            ]
        ]
        await target_msg.reply_html(card_text, reply_markup=InlineKeyboardMarkup(card_buttons))

    # Bottom navigation menu
    bottom_markup = InlineKeyboardMarkup(filter_buttons + [
        [
            InlineKeyboardButton("🔄 Ro'yxatni Yangilash", callback_data=f"w_filter_{filter_mode.lower()}"),
            InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")
        ]
    ])
    await target_msg.reply_html("<i>Boshqa toifadagi ishlarni ko'rish:</i>", reply_markup=bottom_markup)

async def worker_jobs_filter_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == 'w_filter_matched':
        return await render_worker_jobs_feed(update, context, filter_mode='MATCHED')
    elif data == 'w_filter_nearby':
        return await render_worker_jobs_feed(update, context, filter_mode='NEARBY')
    elif data == 'w_filter_all':
        return await render_worker_jobs_feed(update, context, filter_mode='ALL')
    elif data == 'w_filter_cats':
        return await show_category_picker_callback(update, context)
    elif data.startswith('w_filter_cat_'):
        cat_id = int(data.split('_')[3])
        return await render_worker_jobs_feed(update, context, filter_mode='CATEGORY', cat_id=cat_id)

async def show_category_picker_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cats_with_counts = await get_categories_with_job_counts()
    buttons = []
    
    # 2 columns per row
    row = []
    for cat, count in cats_with_counts:
        badge = f" ({count})" if count > 0 else ""
        row.append(InlineKeyboardButton(f"{cat.icon} {cat.name}{badge}", callback_data=f"w_filter_cat_{cat.id}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton("◀️ Orqaga (Ishlarga)", callback_data="w_filter_matched"),
        InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")
    ])

    text = (
        "📂 <b>QAYSI SOHADAGI ISHLARNI KO'RMOQCHISIZ?</b>\n\n"
        "Kerakli xizmat yo'nalishini tanlang:"
    )
    await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))

async def accept_job_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split('_')[2])

    success, result = await accept_job_by_worker(query.from_user.id, order_id)
    if not success:
        await query.edit_message_text(f"⚠️ <b>Xatolik:</b> {result}", parse_mode='HTML')
        return

    order = result
    user = await get_or_create_worker_user(query.from_user)
    kb = get_worker_keyboard(user)

    success_text = (
        f"🎉 <b>TABRIKLAYMIZ! SIZ ISHNI QABUL QILDINGIZ (#ID: #{order.id})</b>\n\n"
        f"📌 <b>Nom:</b> {order.title}\n"
        f"👤 <b>Mijoz:</b> {order.customer_name}\n"
        f"📞 <b>Mijoz Telefoni:</b> <code>{order.customer_phone}</code>\n"
        f"📍 <b>Manzil:</b> {order.address}\n"
        f"💰 <b>Narx:</b> {order.price:,.0f} SUM\n\n"
        "<i>Iltimos, zudlik bilan mijoz bilan bog'laning va ishni boshlang!</i>"
    )

    action_buttons = [
        [
            InlineKeyboardButton(f"📞 Mijozga Qo'ng'iroq", url=f"https://t.me/share/url?url=Tel:{order.customer_phone}"),
            InlineKeyboardButton("🏁 Ishni Yakunlash", callback_data=f"finish_order_{order.id}")
        ],
        [InlineKeyboardButton("📋 Mening Ishlarim", callback_data="go_my_jobs")]
    ]
    markup = InlineKeyboardMarkup(action_buttons)

    await query.edit_message_text(success_text, parse_mode='HTML', reply_markup=markup)
    await query.message.reply_text("Amallar menyusi:", reply_markup=kb)

async def check_job_status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split('_')[2])

    order = await check_order_status_db(order_id)
    if not order:
        await query.answer("Buyurtma topilmadi!", show_alert=True)
        return

    if order.status == Order.Status.PENDING:
        await query.answer("🟢 Ushbu buyurtma hali ham bo'sh! Tezroq qabul qiling.", show_alert=True)
    else:
        status_map = {
            'DISPATCHED': 'boshqa usta tomonidan qabul qilingan',
            'STARTED': 'hozirda bajarilmoqda',
            'FINISHED': 'yakunlangan',
            'CANCELLED': 'bekor qilingan'
        }
        st_text = status_map.get(order.status, order.status)
        await query.answer(f"⚠️ Ushbu buyurtma allaqachon {st_text}!", show_alert=True)
        await query.edit_message_text(f"⚠️ <b>Buyurtma #{order_id}</b> allaqachon {st_text}.", parse_mode='HTML')

# --- MENING ISHLARIM (WORKER'S ACCEPTED JOBS) ---

async def my_jobs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_worker_user(update.effective_user if update.effective_user else update.callback_query.from_user)

    text = (
        "<b>📋 SIZNING ISHLARINGIZ BOSHQARUVI</b>\n\n"
        "Quyidagi bo'limlardan birini tanlang:"
    )

    buttons = [
        [
            InlineKeyboardButton("🟣 Hozirgi Jarayondagi Ishlar", callback_data="w_jobs_active"),
            InlineKeyboardButton("🟢 Yakunlangan Ishlar", callback_data="w_jobs_finished")
        ],
        [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
    ]

    markup = InlineKeyboardMarkup(buttons)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=markup)
    else:
        await update.message.reply_html(text, reply_markup=markup)

async def worker_jobs_nav_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'w_jobs_active':
        orders = await get_worker_my_jobs(query.from_user.id, 'ACTIVE')
        title = "🟣 SIZNING FAOL ISHLARINGIZ"
    else:
        orders = await get_worker_my_jobs(query.from_user.id, 'FINISHED')
        title = "🟢 SIZNING YAKUNLANGAN ISHLARINGIZ"

    if not orders:
        text = f"<b>{title}</b>\n\nBu bo'limda hozircha buyurtmalar mavjud emas."
        buttons = [
            [InlineKeyboardButton("◀️ Orqaga", callback_data="go_my_jobs")],
            [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
        ]
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))
        return

    await query.edit_message_text(f"<b>{title} ({len(orders)} ta):</b>", parse_mode='HTML')

    for o in orders:
        created_str = o.created_at.strftime("%d.%m.%Y %H:%M") if hasattr(o, 'created_at') and o.created_at else ''
        msg = (
            f"<b>🆔 ISH RAQAMI: #{o.id}</b>\n"
            f"📌 <b>Nom:</b> {o.title}\n"
            f"👤 <b>Mijoz:</b> {o.customer_name}\n"
            f"📞 <b>Telefon:</b> <code>{o.customer_phone}</code>\n"
            f"📍 <b>Manzil:</b> {o.address}\n"
            f"💰 <b>Narxi:</b> {o.price:,.0f} SUM\n"
            f"📅 <b>Vaqt:</b> {created_str}\n"
        )
        buttons = []
        if o.status in [Order.Status.DISPATCHED, Order.Status.STARTED]:
            buttons.append([
                InlineKeyboardButton("📞 Mijozga Tel", url=f"https://t.me/share/url?url=Tel:{o.customer_phone}"),
                InlineKeyboardButton("🏁 Ishni Yakunlash", callback_data=f"finish_order_{o.id}")
            ])
        markup = InlineKeyboardMarkup(buttons) if buttons else None
        await query.message.reply_html(msg, reply_markup=markup)

    bottom_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ Orqaga", callback_data="go_my_jobs"), InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
    ])
    await query.message.reply_html("<i>Boshqa bo'limga o'tish:</i>", reply_markup=bottom_markup)

async def finish_order_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    order_id = int(query.data.split('_')[2])

    success, result = await finish_job_by_worker(query.from_user.id, order_id)
    if not success:
        await query.answer(f"Xatolik: {result}", show_alert=True)
        return

    order = result
    await query.edit_message_text(
        f"✅ <b>Buyurtma #{order.id} muvaffaqiyatli yakunlandi!</b>\n"
        f"💰 Ish summasi: <b>{order.price:,.0f} SUM</b>\n"
        "Xizmatingiz uchun tashakkur!",
        parse_mode='HTML'
    )

# --- ONLINE / OFFLINE TOGGLE ---

async def handle_online_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_online = await toggle_worker_online(update.effective_user.id)
    user = await get_or_create_worker_user(update.effective_user)
    kb = get_worker_keyboard(user)

    if is_online:
        text = "🟢 <b>Siz ONLINE holatiga o'tdingiz!</b>\nEndi yangi buyurtmalar to'g'ridan-to'g'ri sizga kelib tushadi."
    else:
        text = "🔴 <b>Siz OFFLINE (dam olish) holatiga o'tdingiz.</b>\nBuyurtmalar vaqtincha sizga yuborilmaydi."

    await update.message.reply_html(text, reply_markup=kb)

async def callback_toggle_online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    is_online = await toggle_worker_online(query.from_user.id)
    user = await get_or_create_worker_user(query.from_user)
    kb = get_worker_keyboard(user)

    status_str = "🟢 Online" if is_online else "🔴 Offline"
    await query.answer(f"Holatingiz o'zgartirildi: {status_str}", show_alert=True)
    return await profile_command(update, context)

# --- GPS LOCATION UPDATER ---

async def gps_update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loc_btn = KeyboardButton("📍 Joriy GPS Joylashuvni Yuborish", request_location=True)
    cancel_btn = KeyboardButton("❌ Bekor Qilish / Orqaga")
    kb = ReplyKeyboardMarkup([[loc_btn], [cancel_btn]], resize_keyboard=True)

    await update.message.reply_html(
        "📍 <b>Joriy GPS joylashuvingizni yangilang:</b>\n\n"
        "Bu orqali mijozlar sizni xaritada eng yaqin usta sifatida ko'rishadi va buyurtmalar sizga birinchi bo'lib taqsimlanadi.",
        reply_markup=kb
    )
    return WORKER_UPDATE_LOC

async def gps_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_worker_user(update.effective_user)
    kb = get_worker_keyboard(user)

    if update.message.location:
        lat = update.message.location.latitude
        lng = update.message.location.longitude
        await update_worker_location_db(update.effective_user.id, lat, lng)
        await update.message.reply_html(
            f"✅ <b>GPS Joylashuvingiz muvaffaqiyatli yangilandi!</b>\n"
            f"📍 Koordinatalar: <code>{lat:.5f}, {lng:.5f}</code>",
            reply_markup=kb
        )
        return ConversationHandler.END
    else:
        text = update.message.text.strip()
        if "bekor" in text.lower() or text.startswith("❌"):
            await update.message.reply_text("Joylashuv yangilash bekor qilindi.", reply_markup=kb)
            return ConversationHandler.END
        await update.message.reply_html("⚠️ Iltimos, pastdagi <b>«Joriy GPS Joylashuvni Yuborish»</b> tugmasini bosing.", reply_markup=kb)
        return ConversationHandler.END

# --- WORKER PROFILE ---

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_worker_user(update.effective_user if update.effective_user else update.callback_query.from_user)
    status_emoji = "🟢 Online (Faol)" if user.is_online else "🔴 Offline (Dam olishda)"
    cat_name = user.category.name if user.category else (user.specialty or '⚠️ Belgilanmagan')

    text = (
        "<b>👤 USTA SHAXSIY PROFILI</b>\n\n"
        f"🆔 <b>ID:</b> <code>{user.telegram_id}</code>\n"
        f"👤 <b>F.I.Sh:</b> {user.first_name} {user.last_name}\n"
        f"📞 <b>Telefon:</b> {user.phone_number or '⚠️ Kiritilmagan'}\n"
        f"🛠️ <b>Mutaxassislik:</b> <b>{cat_name}</b>\n"
        f"⭐ <b>Reyting:</b> {user.rating} / 5.0\n"
        f"📶 <b>Holat:</b> {status_emoji}\n"
    )

    toggle_btn_text = "🔴 Offline Bo'lish" if user.is_online else "🟢 Online Bo'lish"
    inline_buttons = [
        [
            InlineKeyboardButton("✏️ Ismni Tahrirlash", callback_data="w_edit_name"),
            InlineKeyboardButton("📱 Telefonni Yangilash", callback_data="w_edit_phone")
        ],
        [
            InlineKeyboardButton("🛠️ Mutaxassislikni O'zgartirish", callback_data="w_edit_cat"),
            InlineKeyboardButton(toggle_btn_text, callback_data="w_toggle_online")
        ],
        [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
    ]

    inline_markup = InlineKeyboardMarkup(inline_buttons)
    if update.message:
        await update.message.reply_html(text, reply_markup=inline_markup)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=inline_markup)

async def edit_worker_name_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cancel_kb = ReplyKeyboardMarkup([["❌ Bekor Qilish / Orqaga"]], resize_keyboard=True)
    await query.message.reply_html(
        "✏️ <b>Yangi ism-familiyangizni kiriting:</b>\n"
        "<i>(Masalan: Jamshid Aliyev)</i>",
        reply_markup=cancel_kb
    )
    return WORKER_EDIT_NAME

async def worker_name_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = await get_or_create_worker_user(update.effective_user)
    kb = get_worker_keyboard(user)

    if text.startswith("❌") or "bekor" in text.lower():
        await update.message.reply_text("Tahrirlash bekor qilindi.", reply_markup=kb)
        return ConversationHandler.END

    new_name = text
    user = await update_worker_name(update.effective_user.id, new_name)
    await update.message.reply_html(f"✅ <b>Ismingiz yangilandi:</b> {new_name}", reply_markup=kb)
    return ConversationHandler.END

async def edit_worker_phone_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    loc_btn = KeyboardButton("📞 Telefon Raqamni Yuborish", request_contact=True)
    cancel_btn = KeyboardButton("❌ Bekor Qilish / Orqaga")
    reply_kb = ReplyKeyboardMarkup([[loc_btn], [cancel_btn]], resize_keyboard=True, one_time_keyboard=True)
    await query.message.reply_html(
        "📱 <b>Yangi telefon raqamingizni kiriting yoki pastdagi tugmani bosing:</b>\n"
        "<i>(Masalan: +998901234567)</i>",
        reply_markup=reply_kb
    )
    return WORKER_EDIT_PHONE

async def worker_phone_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_worker_user(update.effective_user)
    kb = get_worker_keyboard(user)

    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        text = update.message.text.strip()
        if text.startswith("❌") or "bekor" in text.lower():
            await update.message.reply_text("Tahrirlash bekor qilindi.", reply_markup=kb)
            return ConversationHandler.END
        phone = text.replace('📞', '').strip()

    user = await update_worker_phone(update.effective_user.id, phone)
    await update.message.reply_html(f"✅ <b>Telefon raqamingiz yangilandi:</b> {phone}", reply_markup=kb)
    return ConversationHandler.END

async def edit_worker_cat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    categories = await get_active_categories()
    buttons = []
    for cat in categories:
        buttons.append([InlineKeyboardButton(f"{cat.icon} {cat.name}", callback_data=f"w_reg_cat_{cat.id}")])
    buttons.append([InlineKeyboardButton("◀️ Orqaga", callback_data="go_profile")])
    await query.edit_message_text(
        "🛠️ <b>Yangi mutaxassislik sohangizni tanlang:</b>",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def callback_go_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = await get_or_create_worker_user(query.from_user)
    kb = get_worker_keyboard(user)
    try:
        await query.delete_message()
    except Exception:
        pass
    await query.message.reply_html("🏠 <b>Usta Bosh Menyu:</b>", reply_markup=kb)

async def cancel_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_worker_user(update.effective_user)
    kb = get_worker_keyboard(user)
    context.user_data.clear()
    await update.message.reply_html("❌ <b>Jarayon bekor qilindi.</b>", reply_markup=kb)
    return ConversationHandler.END

# --- SETUP WORKER BOT APPLICATION ---

def build_worker_bot_application(token: str):
    if not token or not token.strip():
        return None

    app = ApplicationBuilder().token(token.strip()).build()

    edit_name_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_worker_name_callback, pattern='^w_edit_name$')],
        states={
            WORKER_EDIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, worker_name_received)]
        },
        fallbacks=[CommandHandler('cancel', cancel_flow), MessageHandler(filters.Regex('^❌'), cancel_flow)],
        allow_reentry=True
    )

    edit_phone_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_worker_phone_callback, pattern='^w_edit_phone$')],
        states={
            WORKER_EDIT_PHONE: [MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), worker_phone_received)]
        },
        fallbacks=[CommandHandler('cancel', cancel_flow), MessageHandler(filters.Regex('^❌'), cancel_flow)],
        allow_reentry=True
    )

    gps_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('(?i).*(gps|joylashuv|lokatsiya).*'), gps_update_command)],
        states={
            WORKER_UPDATE_LOC: [
                MessageHandler(filters.LOCATION, gps_received),
                MessageHandler(filters.TEXT & ~filters.COMMAND, gps_received)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel_flow), MessageHandler(filters.Regex('^❌'), cancel_flow)],
        allow_reentry=True
    )

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('profile', profile_command))
    app.add_handler(CommandHandler('jobs', search_jobs_command))
    app.add_handler(CommandHandler('myjobs', my_jobs_command))

    app.add_handler(edit_name_handler)
    app.add_handler(edit_phone_handler)
    app.add_handler(gps_handler)

    app.add_handler(CallbackQueryHandler(worker_reg_cat_callback, pattern='^w_reg_cat_'))
    app.add_handler(CallbackQueryHandler(worker_jobs_filter_callback, pattern='^w_filter_'))
    app.add_handler(CallbackQueryHandler(search_jobs_command, pattern='^refresh_search_jobs$'))
    app.add_handler(CallbackQueryHandler(accept_job_callback, pattern='^accept_job_'))
    app.add_handler(CallbackQueryHandler(check_job_status_callback, pattern='^check_job_'))
    app.add_handler(CallbackQueryHandler(finish_order_callback, pattern='^finish_order_'))
    app.add_handler(CallbackQueryHandler(worker_jobs_nav_callback, pattern='^w_jobs_'))
    app.add_handler(CallbackQueryHandler(my_jobs_command, pattern='^go_my_jobs$'))
    app.add_handler(CallbackQueryHandler(profile_command, pattern='^go_profile$'))
    app.add_handler(CallbackQueryHandler(edit_worker_cat_callback, pattern='^w_edit_cat$'))
    app.add_handler(CallbackQueryHandler(callback_toggle_online, pattern='^w_toggle_online$'))
    app.add_handler(CallbackQueryHandler(callback_go_main_menu, pattern='^go_main_menu$'))

    app.add_handler(MessageHandler(filters.Regex('(?i).*(online|offline|bo\'lish|rejim|🟢|🔴).*'), handle_online_toggle))
    app.add_handler(MessageHandler(filters.Regex("(?i).*(qidirish|ishlar|yangi ish).*"), search_jobs_command))
    app.add_handler(MessageHandler(filters.Regex("(?i).*(mening ishlarim|ishlarim).*"), my_jobs_command))
    app.add_handler(MessageHandler(filters.Regex("(?i).*(profil|usta profili).*"), profile_command))
    app.add_handler(MessageHandler(filters.Regex("(?i).*(call center|aloqa|yordam).*"), help_command))

    return app
