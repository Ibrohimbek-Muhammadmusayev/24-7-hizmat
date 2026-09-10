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
from bot_control.models import BotConfig

logger = logging.getLogger(__name__)

# --- CONVERSATION STATES ---
(
    CAT_SELECT,
    WORK_FORMAT,
    TITLE,
    DESC,
    LOC_CHOICE,
    LOCATION,
    CONTACT,
    PRICE,
    CONFIRM,
    EDIT_JOB_TITLE,
    EDIT_JOB_DESC,
    EDIT_JOB_LOC,
    EDIT_JOB_PHONE,
    EDIT_JOB_PRICE,
    EDIT_NAME_STATE,
    EDIT_PHONE_STATE,
    SEARCH_ORDER_ID_STATE,
) = range(17)

# --- KEYBOARDS ---

def get_client_keyboard(user=None):
    row1 = [KeyboardButton("🛠️ Buyurtma Berish"), KeyboardButton("📜 Buyurtmalarim")]
    row2 = [KeyboardButton("💳 Kreditlarim / Balans"), KeyboardButton("👤 Profilim")]
    row3 = [KeyboardButton("📞 Call Center"), KeyboardButton("ℹ️ Biz Haqimizda")]
    return ReplyKeyboardMarkup([row1, row2, row3], resize_keyboard=True)

# --- DB HELPERS ---

@sync_to_async
def get_bot_config():
    return BotConfig.get_config()

@sync_to_async
def get_or_create_client_user(tg_user):
    config = BotConfig.get_config()
    user, created = User.objects.get_or_create(
        telegram_id=tg_user.id,
        defaults={
            'username': f"tg_{tg_user.id}",
            'first_name': tg_user.first_name or '',
            'last_name': tg_user.last_name or '',
            'role': User.Role.CLIENT,
            'job_credits': config.initial_free_credits,
            'started_client_bot': True,
        }
    )
    if not user.started_client_bot:
        user.started_client_bot = True
        user.save()
    return user

@sync_to_async
def get_active_categories():
    return list(Category.objects.filter(is_active=True))

@sync_to_async
def get_category_by_id(cat_id):
    return Category.objects.filter(id=cat_id).first()

@sync_to_async
def update_user_name(tg_id, new_name):
    user = User.objects.filter(telegram_id=tg_id).first()
    if user:
        user.first_name = new_name
        user.save()
        return user
    return None

@sync_to_async
def update_user_phone(tg_id, phone):
    user = User.objects.filter(telegram_id=tg_id).first()
    if user:
        user.phone_number = phone
        user.save()
        return user
    return None

@sync_to_async
def get_client_orders_filtered(tg_id, filter_type='ALL'):
    qs = Order.objects.select_related('category', 'assigned_worker').filter(customer_telegram_id=tg_id)
    if filter_type == 'ACTIVE':
        qs = qs.filter(status__in=[Order.Status.DISPATCHED, Order.Status.STARTED, Order.Status.PENDING])
    elif filter_type == 'FINISHED':
        qs = qs.filter(status=Order.Status.FINISHED)
    return list(qs.order_by('-created_at')[:10])

@sync_to_async
def get_order_by_numeric_id(order_id, tg_id):
    try:
        return Order.objects.select_related('category', 'assigned_worker').filter(id=int(order_id), customer_telegram_id=tg_id).first()
    except Exception:
        return None

@sync_to_async
def create_client_order(user_tg_id, customer_name, phone, cat_id, title, desc, address, lat, lng, price, work_format):
    config = BotConfig.get_config()
    user = User.objects.filter(telegram_id=user_tg_id).first()
    category = Category.objects.filter(id=cat_id).first()

    # If monetization is enabled, deduct credit
    if config.monetization_enabled and user:
        cost = max(1, config.job_posting_cost_credits)
        if user.job_credits >= cost:
            user.job_credits -= cost
            user.save()

    order = Order.objects.create(
        customer_name=customer_name or (user.first_name if user else 'Mijoz'),
        customer_phone=phone or (user.phone_number if user else ''),
        customer_telegram_id=user_tg_id,
        category=category,
        service_type=category.name if category else 'Umumiy xizmat',
        title=title,
        description=desc,
        address=address or 'Toshkent',
        latitude=lat or 41.311081,
        longitude=lng or 69.240562,
        price=price,
        work_format=work_format,
        status=Order.Status.PENDING
    )
    return order, user.job_credits if user else 0

# --- COMMAND HANDLERS ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_client_user(update.effective_user)
    config = await get_bot_config()
    kb = get_client_keyboard(user)

    first_name = update.effective_user.first_name or user.first_name or "Ish Beruvchi"

    monetization_info = ""
    if config.monetization_enabled:
        monetization_info = f"\n💳 <b>Sizning bepul kreditlaringiz:</b> <b>{user.job_credits} ta</b> (1 ish = {config.job_posting_cost_credits} kredit)\n"

    default_text = (
        f"Assalomu alaykum, <b>{first_name}</b>! 👋\n\n"
        "<b>Full-Xizmat (Ish Beruvchilar Boti)</b>ga xush kelibsiz!\n"
        "Ushbu bot orqali usta va mutaxassislarga istalgan turdagi ishlaringizni tezkor joylashingiz mumkin."
        f"{monetization_info}\n"
        "Kerakli bo'limni tanlang:"
    )

    welcome_text = config.welcome_text if config.welcome_text else default_text
    welcome_text = welcome_text.replace("{first_name}", first_name).replace("{id}", str(update.effective_user.id)).replace("{role}", "Ish Beruvchi")

    if config.welcome_image_url and config.welcome_image_url.strip().startswith('http'):
        try:
            await update.message.reply_photo(photo=config.welcome_image_url.strip(), caption=welcome_text, parse_mode='HTML', reply_markup=kb)
            return
        except Exception:
            pass

    await update.message.reply_html(welcome_text, reply_markup=kb)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = await get_bot_config()
    phone = config.call_center_phone or "+998 (71) 200-00-00"
    about = config.about_text or "Full-Xizmat — Ish beruvchilar va ustalarni tezkor bog'lovchi professional platforma."

    text = (
        f"<b>ℹ️ BIZ HAQIMIZDA & CALL CENTER</b>\n\n"
        f"{about}\n\n"
        f"📞 <b>Operator:</b> <code>{phone}</code> (24/7)\n\n"
        "• <b>Buyurtma Berish:</b> Xizmat turini tanlab, e'lon qoldiring.\n"
        "• <b>Kreditlarim:</b> Ish joylash uchun mavjud kreditlaringizni tekshiring.\n"
        "• <b>Buyurtmalarim:</b> Joylangan e'lonlaringiz holatini kuzatib boring."
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

async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_client_user(update.effective_user)
    config = await get_bot_config()

    if config.monetization_enabled:
        st_text = "🟢 <b>FAOL</b>"
        cost_text = f"{config.job_posting_cost_credits} ta kredit"
        price_text = f"{config.credit_price_sum:,.0f} so'm"
    else:
        st_text = "⚪ <b>BEPUL REJIM</b> (Hozirda barcha ishlar bepul joylanadi)"
        cost_text = "0 kredit (Bepul)"
        price_text = "0 so'm"

    phone = config.call_center_phone or "+998 (71) 200-00-00"

    text = (
        "<b>💳 SIZNING BALANSINGIZ VA KREDITLARINGIZ</b>\n\n"
        f"📊 <b>Mavjud Kreditlar:</b> <b>{user.job_credits} ta</b>\n"
        f"⚙️ <b>Tizim Holati:</b> {st_text}\n"
        f"💰 <b>1 ta ish joylash:</b> {cost_text}\n"
        f"💵 <b>1 ta kredit narxi:</b> {price_text}\n\n"
        "<i>Kredit sotib olish yoki hisobni to'ldirish uchun operator bilan bog'laning:</i>"
    )

    inline_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"📞 Operatorga Bog'lanish ({phone})", url=f"https://t.me/share/url?url=Tel:{phone}")],
        [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
    ])

    if update.message:
        await update.message.reply_html(text, reply_markup=inline_kb)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=inline_kb)

# --- PROFILE ---

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_client_user(update.effective_user if update.effective_user else update.callback_query.from_user)

    text = (
        "<b>👤 ISH BERUVCHI PROFILI</b>\n\n"
        f"🆔 <b>ID:</b> <code>{user.telegram_id}</code>\n"
        f"👤 <b>F.I.Sh:</b> {user.first_name} {user.last_name}\n"
        f"📞 <b>Telefon:</b> {user.phone_number or '⚠️ Kiritilmagan'}\n"
        f"🎭 <b>Maqom:</b> 💼 Ish Beruvchi / Mijoz\n"
        f"💳 <b>Mavjud Kreditlar:</b> <b>{user.job_credits} ta</b>\n"
    )

    inline_buttons = [
        [
            InlineKeyboardButton("✏️ Ismni O'zgartirish", callback_data="edit_profile_name"),
            InlineKeyboardButton("📱 Telefonni Yangilash", callback_data="edit_profile_phone")
        ],
        [
            InlineKeyboardButton("💳 Kreditlarim", callback_data="go_credits"),
            InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")
        ]
    ]

    inline_markup = InlineKeyboardMarkup(inline_buttons)
    if update.message:
        await update.message.reply_html(text, reply_markup=inline_markup)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=inline_markup)

async def edit_name_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cancel_kb = ReplyKeyboardMarkup([["❌ Bekor Qilish / Orqaga"]], resize_keyboard=True)
    await query.message.reply_html(
        "✏️ <b>Yangi ism-familiyangizni kiriting:</b>\n"
        "<i>(Masalan: Sardor Rahimov)</i>",
        reply_markup=cancel_kb
    )
    return EDIT_NAME_STATE

async def name_edited_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.startswith("❌") or "bekor" in text.lower():
        user = await get_or_create_client_user(update.effective_user)
        kb = get_client_keyboard(user)
        await update.message.reply_text("Tahrirlash bekor qilindi.", reply_markup=kb)
        return ConversationHandler.END

    new_name = text
    user = await update_user_name(update.effective_user.id, new_name)
    kb = get_client_keyboard(user)
    await update.message.reply_html(f"✅ <b>Ismingiz yangilandi:</b> {new_name}", reply_markup=kb)
    return ConversationHandler.END

async def edit_phone_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    return EDIT_PHONE_STATE

async def phone_edited_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        text = update.message.text.strip()
        if text.startswith("❌") or "bekor" in text.lower():
            user = await get_or_create_client_user(update.effective_user)
            kb = get_client_keyboard(user)
            await update.message.reply_text("Tahrirlash bekor qilindi.", reply_markup=kb)
            return ConversationHandler.END
        phone = text.replace('📞', '').strip()

    user = await update_user_phone(update.effective_user.id, phone)
    kb = get_client_keyboard(user)
    await update.message.reply_html(f"✅ <b>Telefon raqamingiz yangilandi:</b> {phone}", reply_markup=kb)
    return ConversationHandler.END

# --- BUYURTMA BERISH (JOB POSTING WITH CREDIT VALIDATION) ---

async def start_job_posting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    user = await get_or_create_client_user(update.effective_user)
    config = await get_bot_config()

    # Check credit balance if monetization is enabled
    if config.monetization_enabled:
        cost = max(1, config.job_posting_cost_credits)
        if user.job_credits < cost:
            phone = config.call_center_phone or "+998 (71) 200-00-00"
            text = (
                "⚠️ <b>KREDITLARINGIZ YETARLI EMAS!</b>\n\n"
                f"Sizning balansingiz: <b>{user.job_credits} ta kredit</b>\n"
                f"1 ta ish joylash narxi: <b>{cost} ta kredit</b>\n\n"
                "Ish joylash uchun hisobingizni to'ldirishingiz kerak. Iltimos, operator bilan bog'laning:"
            )
            inline_kb = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"📞 Hisobni To'ldirish ({phone})", url=f"https://t.me/share/url?url=Tel:{phone}")],
                [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
            ])
            await update.message.reply_html(text, reply_markup=inline_kb)
            return ConversationHandler.END

    categories = await get_active_categories()
    if not categories:
        await update.message.reply_text("Hozircha xizmat toifalari mavjud emas.")
        return ConversationHandler.END

    buttons = []
    for cat in categories:
        buttons.append([InlineKeyboardButton(f"{cat.icon} {cat.name}", callback_data=f"cat_{cat.id}")])
    buttons.append([InlineKeyboardButton("❌ Bekor Qilish", callback_data="cancel_flow")])

    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_html(
        "📂 <b>Xizmat toifasini tanlang:</b>",
        reply_markup=markup
    )
    return CAT_SELECT

async def cat_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat_id = int(query.data.split('_')[1])
    context.user_data['job_cat_id'] = cat_id

    cat = await get_category_by_id(cat_id)
    try:
        await query.delete_message()
    except Exception:
        pass

    format_kb = ReplyKeyboardMarkup([
        ["📍 Joyida (Offline)", "💻 Masofaviy (Online)"],
        ["❌ Bekor Qilish"]
    ], resize_keyboard=True)

    await query.message.reply_html(
        f"Tanlangan xizmat: <b>{cat.name}</b>\n\n"
        "🌐 <b>Xizmat formatini tanlang:</b>",
        reply_markup=format_kb
    )
    return WORK_FORMAT

async def work_format_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        fmt = query.data.split('_')[1]
        msg = query.message
    else:
        text = update.message.text.strip()
        if text == "❌ Bekor Qilish":
            return await cancel_flow(update, context)
        if "orqaga" in text.lower():
            return await render_order_confirmation(update, context)
        fmt = 'ONLINE' if 'online' in text.lower() or 'masofaviy' in text.lower() else 'OFFLINE'
        msg = update.message

    context.user_data['job_work_format'] = fmt
    fmt_label = "📍 Joyida (Offline)" if fmt == 'OFFLINE' else "💻 Masofaviy (Online)"

    if context.user_data.get('job_title'):
        if fmt == 'ONLINE':
            context.user_data['job_address'] = '💻 Masofaviy (Online)'
        return await render_order_confirmation(update, context)

    cancel_kb = ReplyKeyboardMarkup([["❌ Bekor Qilish"]], resize_keyboard=True)
    await msg.reply_html(
        f"Format: <b>{fmt_label}</b>\n\n"
        "📝 <b>Ish nomini yozing:</b>\n<i>(Masalan: Kran tuzatish)</i>",
        reply_markup=cancel_kb
    )
    return TITLE

async def title_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "❌ Bekor Qilish":
        return await cancel_flow(update, context)

    context.user_data['job_title'] = text
    cancel_kb = ReplyKeyboardMarkup([["❌ Bekor Qilish"]], resize_keyboard=True)
    await update.message.reply_html(
        "📄 <b>Batafsil ma'lumot yozing:</b>\n<i>(Masalan: Oshxonadagi suv quvuri oqayapti)</i>",
        reply_markup=cancel_kb
    )
    return DESC

async def desc_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "❌ Bekor Qilish":
        return await cancel_flow(update, context)

    context.user_data['job_desc'] = text

    if context.user_data.get('job_work_format') == 'ONLINE':
        context.user_data['job_address'] = '💻 Masofaviy (Online)'
        context.user_data['job_lat'] = 41.311081
        context.user_data['job_lng'] = 69.240562
        return await ask_contact(update, context)

    loc_btn = KeyboardButton("📍 Joriy GPS", request_location=True)
    map_btn = KeyboardButton("🗺️ Xaritadan tanlash")
    text_btn = KeyboardButton("✍️ Manzil yozish")
    cancel_btn = KeyboardButton("❌ Bekor Qilish")
    kb = ReplyKeyboardMarkup([[loc_btn], [map_btn, text_btn], [cancel_btn]], resize_keyboard=True)

    await update.message.reply_html(
        "📍 <b>Joylashuvni tanlang:</b>",
        reply_markup=kb
    )
    return LOC_CHOICE

async def loc_choice_or_direct_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.location:
        lat = update.message.location.latitude
        lng = update.message.location.longitude
        context.user_data['job_lat'] = lat
        context.user_data['job_lng'] = lng
        if update.message.venue and update.message.venue.title:
            context.user_data['job_address'] = f"{update.message.venue.title}, {update.message.venue.address or ''}"
        else:
            context.user_data['job_address'] = f"GPS: {lat:.5f}, {lng:.5f}"
        return await ask_contact(update, context)

    text = update.message.text.strip()
    if text == "❌ Bekor Qilish":
        return await cancel_flow(update, context)
    elif text == "🗺️ Xaritadan tanlash":
        loc_btn = KeyboardButton("📍 Joriy GPS", request_location=True)
        cancel_btn = KeyboardButton("❌ Bekor Qilish")
        await update.message.reply_html(
            "🗺️ <b>Xaritadan tanlash:</b>\n"
            "📎 Skrepka ➔ 📍 Joylashuv ➔ Kerakli nuqtani tanlab yuboring.",
            reply_markup=ReplyKeyboardMarkup([[loc_btn], [cancel_btn]], resize_keyboard=True)
        )
        return LOCATION
    elif text == "✍️ Manzil yozish":
        cancel_kb = ReplyKeyboardMarkup([["❌ Bekor Qilish"]], resize_keyboard=True)
        await update.message.reply_html(
            "✍️ <b>Manzilni yozing:</b>\n<i>(Masalan: Chilonzor 9-mavze, 25-uy)</i>",
            reply_markup=cancel_kb
        )
        return LOCATION
    elif text == "📍 Joriy GPS":
        loc_btn = KeyboardButton("📍 GPS Yuborish", request_location=True)
        cancel_btn = KeyboardButton("❌ Bekor Qilish")
        await update.message.reply_text(
            "Pastdagi tugmani bosing:",
            reply_markup=ReplyKeyboardMarkup([[loc_btn], [cancel_btn]], resize_keyboard=True)
        )
        return LOCATION
    else:
        context.user_data['job_address'] = text
        context.user_data['job_lat'] = 41.311081
        context.user_data['job_lng'] = 69.240562
        return await ask_contact(update, context)

async def location_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.location:
        lat = update.message.location.latitude
        lng = update.message.location.longitude
        context.user_data['job_lat'] = lat
        context.user_data['job_lng'] = lng
        if update.message.venue and update.message.venue.title:
            context.user_data['job_address'] = f"{update.message.venue.title}, {update.message.venue.address or ''}"
        else:
            context.user_data['job_address'] = f"GPS: {lat:.5f}, {lng:.5f}"
    else:
        text = update.message.text.strip()
        if text == "❌ Bekor Qilish":
            return await cancel_flow(update, context)
        context.user_data['job_address'] = text
        context.user_data['job_lat'] = 41.311081
        context.user_data['job_lng'] = 69.240562

    return await ask_contact(update, context)

async def ask_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_client_user(update.effective_user)
    buttons = [[KeyboardButton("📞 Raqamni yuborish", request_contact=True)]]
    if user.phone_number:
        buttons.append([KeyboardButton(f"📞 {user.phone_number}")])
    buttons.append([KeyboardButton("❌ Bekor Qilish")])

    kb = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_html(
        "📞 <b>Telefon raqamingizni yuboring:</b>",
        reply_markup=kb
    )
    return CONTACT

async def contact_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        text = update.message.text.strip()
        if text == "❌ Bekor Qilish":
            return await cancel_flow(update, context)
        phone = text.replace('📞', '').strip()

    context.user_data['job_phone'] = phone
    await update_user_phone(update.effective_user.id, phone)

    await update.message.reply_html(
        "💰 <b>Taklif narxini tanlang yoki yozing (SUM):</b>",
        reply_markup=ReplyKeyboardMarkup([['50 000', '100 000', '200 000', '300 000'], ['❌ Bekor Qilish']], resize_keyboard=True)
    )
    return PRICE

async def render_order_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE, is_edit=False):
    cat_id = context.user_data.get('job_cat_id')
    cat = await get_category_by_id(cat_id) if cat_id else None
    cat_name = cat.name if cat else 'Umumiy'

    fmt = context.user_data.get('job_work_format', 'OFFLINE')
    fmt_label = "📍 Joyida (Offline)" if fmt == 'OFFLINE' else "💻 Masofaviy (Online)"

    title = context.user_data.get('job_title', 'Nom kiritilmagan')
    desc = context.user_data.get('job_desc', 'Tavsif yo\'q')
    address = context.user_data.get('job_address', 'Manzil yo\'q')
    phone = context.user_data.get('job_phone', 'Telefon yo\'q')
    price = context.user_data.get('job_price', 50000.0)

    config = await get_bot_config()
    cost_str = f" ({config.job_posting_cost_credits} kredit yechiladi)" if config.monetization_enabled else " (Bepul)"

    summary_html = (
        "<b>📋 BUYURTMA MA'LUMOTLARINI TASDIQLANG:</b>\n\n"
        f"1️⃣ 📂 <b>Xizmat:</b> {cat_name}\n"
        f"2️⃣ 🌐 <b>Format:</b> {fmt_label}\n"
        f"3️⃣ 📝 <b>Nom:</b> {title}\n"
        f"4️⃣ 📄 <b>Tavsif:</b> {desc}\n"
        f"5️⃣ 📍 <b>Manzil:</b> {address}\n"
        f"6️⃣ 📞 <b>Telefon:</b> {phone}\n"
        f"7️⃣ 💰 <b>Narx:</b> <b>{price:,.0f} so'm</b>\n\n"
        f"<i>Barcha ma'lumotlar to'g'ri bo'lsa <b>«Tasdiqlash & Joylash»{cost_str}</b> tugmasini bosing:</i>"
    )

    confirm_kb = ReplyKeyboardMarkup([
        ["✅ Tasdiqlash & Joylash"],
        ["✏️ Ma'lumotlarni Tahrirlash"],
        ["❌ Bekor Qilish"]
    ], resize_keyboard=True)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_html(summary_html, reply_markup=confirm_kb)
    else:
        await update.message.reply_html(summary_html, reply_markup=confirm_kb)

    return CONFIRM

async def price_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "❌ Bekor Qilish":
        return await cancel_flow(update, context)

    try:
        price = float(text.replace(' ', ''))
    except ValueError:
        price = 50000.0

    context.user_data['job_price'] = price
    return await render_order_confirmation(update, context)

async def confirm_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = await get_or_create_client_user(update.effective_user)
    kb = get_client_keyboard(user)

    if text.startswith("✅") or "tasdiqlash" in text.lower():
        order, remaining_credits = await create_client_order(
            user_tg_id=update.effective_user.id,
            customer_name=update.effective_user.first_name,
            phone=context.user_data.get('job_phone', ''),
            cat_id=context.user_data.get('job_cat_id', 1),
            title=context.user_data.get('job_title', 'Xizmat'),
            desc=context.user_data.get('job_desc', ''),
            address=context.user_data.get('job_address', ''),
            lat=context.user_data.get('job_lat', 41.311081),
            lng=context.user_data.get('job_lng', 69.240562),
            price=context.user_data.get('job_price', 50000.0),
            work_format=context.user_data.get('job_work_format', 'OFFLINE')
        )
        fmt_label = '📍 Joyida (Offline)' if order.work_format == 'OFFLINE' else '💻 Masofaviy (Online)'
        
        config = await get_bot_config()
        credit_msg = f"\n💳 <b>Qolgan kreditlaringiz:</b> <b>{remaining_credits} ta</b>\n" if config.monetization_enabled else ""

        await update.message.reply_html(
            f"🎉 <b>Buyurtmangiz qabul qilindi! (#ID: #{order.id})</b>\n\n"
            f"Format: <b>{fmt_label}</b>\n"
            f"{credit_msg}"
            "Yaqin atrofdagi usta tez orada siz bilan bog'lanadi.",
            reply_markup=kb
        )
        context.user_data.clear()
        return ConversationHandler.END

    elif "tahrir" in text.lower():
        edit_menu_kb = ReplyKeyboardMarkup([
            ["📂 1. Kategoriya", "🌐 2. Format"],
            ["📝 3. Nom", "📄 4. Tavsif"],
            ["📍 5. Manzil", "📞 6. Telefon"],
            ["💰 7. Narx", "◀️ Orqaga (Tasdiqlashga)"],
            ["❌ Bekor Qilish"]
        ], resize_keyboard=True)
        await update.message.reply_html(
            "✏️ <b>Qaysi ma'lumotni o'zgartirmoqchisiz?</b>\n"
            "Kerakli bo'limni tanlang:",
            reply_markup=edit_menu_kb
        )
        return CONFIRM

    elif "1. kategoriya" in text.lower() or "kategoriya" in text.lower():
        return await edit_field_cat_callback(update, context)

    elif "2. format" in text.lower() or "format" in text.lower():
        format_kb = ReplyKeyboardMarkup([
            ["📍 Joyida (Offline)", "💻 Masofaviy (Online)"],
            ["◀️ Orqaga (Tasdiqlashga)"]
        ], resize_keyboard=True)
        await update.message.reply_html("🌐 <b>Yangi formatni tanlang:</b>", reply_markup=format_kb)
        return WORK_FORMAT

    elif "3. nom" in text.lower() or "nom" in text.lower():
        cancel_kb = ReplyKeyboardMarkup([["❌ Bekor Qilish"]], resize_keyboard=True)
        await update.message.reply_html("📝 <b>Yangi ish nomini yozing:</b>", reply_markup=cancel_kb)
        return EDIT_JOB_TITLE

    elif "4. tavsif" in text.lower() or "tavsif" in text.lower():
        cancel_kb = ReplyKeyboardMarkup([["❌ Bekor Qilish"]], resize_keyboard=True)
        await update.message.reply_html("📄 <b>Yangi tavsifni yozing:</b>", reply_markup=cancel_kb)
        return EDIT_JOB_DESC

    elif "5. manzil" in text.lower() or "manzil" in text.lower():
        loc_btn = KeyboardButton("📍 Joriy GPS", request_location=True)
        map_btn = KeyboardButton("🗺️ Xaritadan tanlash")
        text_btn = KeyboardButton("✍️ Manzil yozish")
        cancel_btn = KeyboardButton("❌ Bekor Qilish")
        kb = ReplyKeyboardMarkup([[loc_btn], [map_btn, text_btn], [cancel_btn]], resize_keyboard=True)
        await update.message.reply_html("📍 <b>Yangi joylashuvni tanlang:</b>", reply_markup=kb)
        return EDIT_JOB_LOC

    elif "6. telefon" in text.lower() or "telefon" in text.lower():
        loc_btn = KeyboardButton("📞 Raqamni yuborish", request_contact=True)
        cancel_btn = KeyboardButton("❌ Bekor Qilish")
        kb = ReplyKeyboardMarkup([[loc_btn], [cancel_btn]], resize_keyboard=True)
        await update.message.reply_html("📞 <b>Yangi telefon raqamingizni yuboring:</b>", reply_markup=kb)
        return EDIT_JOB_PHONE

    elif "7. narx" in text.lower() or "narx" in text.lower():
        kb = ReplyKeyboardMarkup([['50 000', '100 000', '200 000', '300 000'], ['❌ Bekor Qilish']], resize_keyboard=True)
        await update.message.reply_html("💰 <b>Yangi narxni tanlang yoki yozing:</b>", reply_markup=kb)
        return EDIT_JOB_PRICE

    elif "orqaga" in text.lower():
        return await render_order_confirmation(update, context)

    elif text == "❌ Bekor Qilish":
        return await cancel_flow(update, context)

    else:
        return await render_order_confirmation(update, context)

async def edit_field_cat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    msg = query.message if query else update.message
    if query:
        await query.answer()

    categories = await get_active_categories()
    buttons = []
    for cat in categories:
        buttons.append([InlineKeyboardButton(f"{cat.icon} {cat.name}", callback_data=f"set_field_cat_{cat.id}")])

    await msg.reply_html("🛠️ <b>Yangi xizmat toifasini tanlang:</b>", reply_markup=InlineKeyboardMarkup(buttons))
    return CONFIRM

async def set_field_cat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat_id = int(query.data.split('_')[3])
    context.user_data['job_cat_id'] = cat_id
    try:
        await query.delete_message()
    except Exception:
        pass
    return await render_order_confirmation(update, context)

async def title_edited_in_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "❌ Bekor Qilish":
        return await cancel_flow(update, context)
    context.user_data['job_title'] = text
    return await render_order_confirmation(update, context)

async def desc_edited_in_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "❌ Bekor Qilish":
        return await cancel_flow(update, context)
    context.user_data['job_desc'] = text
    return await render_order_confirmation(update, context)

async def loc_edited_in_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.location:
        lat = update.message.location.latitude
        lng = update.message.location.longitude
        context.user_data['job_lat'] = lat
        context.user_data['job_lng'] = lng
        if update.message.venue and update.message.venue.title:
            context.user_data['job_address'] = f"{update.message.venue.title}, {update.message.venue.address or ''}"
        else:
            context.user_data['job_address'] = f"GPS: {lat:.5f}, {lng:.5f}"
    else:
        text = update.message.text.strip()
        if text == "❌ Bekor Qilish":
            return await cancel_flow(update, context)
        elif text == "🗺️ Xaritadan tanlash":
            loc_btn = KeyboardButton("📍 Joriy GPS", request_location=True)
            cancel_btn = KeyboardButton("❌ Bekor Qilish")
            await update.message.reply_html(
                "🗺️ <b>XARITADAN JOY TANLASH:</b>\n"
                "1️⃣ 📎 Skrepka belgisini bosing ➔ 📍 Joylashuvni tanlang.\n"
                "2️⃣ Xaritadagi markerni kerakli manzil ustiga qo'yib yuboring!",
                reply_markup=ReplyKeyboardMarkup([[loc_btn], [cancel_btn]], resize_keyboard=True)
            )
            return EDIT_JOB_LOC
        elif text == "📍 Joriy GPS":
            loc_btn = KeyboardButton("📍 GPS Yuborish", request_location=True)
            cancel_btn = KeyboardButton("❌ Bekor Qilish")
            await update.message.reply_text("Pastdagi tugmani bosing:", reply_markup=ReplyKeyboardMarkup([[loc_btn], [cancel_btn]], resize_keyboard=True))
            return EDIT_JOB_LOC
        else:
            context.user_data['job_address'] = text
            context.user_data['job_lat'] = 41.311081
            context.user_data['job_lng'] = 69.240562

    return await render_order_confirmation(update, context)

async def phone_edited_in_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        text = update.message.text.strip()
        if text == "❌ Bekor Qilish":
            return await cancel_flow(update, context)
        phone = text.replace('📞', '').strip()

    context.user_data['job_phone'] = phone
    await update_user_phone(update.effective_user.id, phone)
    return await render_order_confirmation(update, context)

async def price_edited_in_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "❌ Bekor Qilish":
        return await cancel_flow(update, context)
    try:
        price = float(text.replace(' ', ''))
    except ValueError:
        price = 50000.0
    context.user_data['job_price'] = price
    return await render_order_confirmation(update, context)

# --- BUYURTMALARIM ---

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "<b>📜 BUYURTMALAR BOSHQARUV MARKAZI</b>\n\n"
        "Quyidagi bo'limlardan birini tanlang yoki aniq ish raqami (ID) bo'yicha qidiring:"
    )

    buttons = [
        [InlineKeyboardButton("🔍 Ish Raqami (ID) Bo'yicha Qidirish", callback_data="orders_nav_search")],
        [
            InlineKeyboardButton("🟣 Jarayondagi Ishlar", callback_data="orders_nav_active"),
            InlineKeyboardButton("🟢 Yakunlangan", callback_data="orders_nav_finished")
        ],
        [InlineKeyboardButton("📋 Barcha Buyurtmalarim", callback_data="orders_nav_all")],
        [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
    ]

    markup = InlineKeyboardMarkup(buttons)
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, parse_mode='HTML', reply_markup=markup)
    else:
        await update.message.reply_html(text, reply_markup=markup)

async def render_client_orders_list(query, orders, title_header):
    if not orders:
        text = f"<b>{title_header}</b>\n\nBu bo'limda hozircha buyurtmalaringiz mavjud emas."
        buttons = [
            [InlineKeyboardButton("◀️ Orqaga (Buyurtmalarim)", callback_data="orders_nav_menu")],
            [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
        ]
        await query.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))
        return

    status_map = {
        'PENDING': '🟡 Ochiq / Usta kutilmoqda',
        'DISPATCHED': '🔵 Usta Biriktirildi',
        'STARTED': '🟣 Ish Bajarilmoqda',
        'FINISHED': '🟢 Yakunlandi',
        'CANCELLED': '🔴 Bekor Qilindi'
    }
    format_map = {
        'OFFLINE': '📍 Joyida (Offline)',
        'ONLINE': '💻 Masofaviy (Online)'
    }

    await query.edit_message_text(f"<b>{title_header} ({len(orders)} ta):</b>", parse_mode='HTML')

    for o in orders:
        st_text = status_map.get(o.status, o.status)
        fmt_text = format_map.get(o.work_format, '📍 Joyida')
        created_str = o.created_at.strftime("%d.%m.%Y %H:%M") if hasattr(o, 'created_at') and o.created_at else ''

        msg = (
            f"<b>🆔 ISH RAQAMI: #{o.id}</b>\n"
            f"📌 <b>Nom:</b> {o.title}\n"
            f"🌐 <b>Format:</b> {fmt_text}\n"
            f"📁 <b>Yo'nalish:</b> {o.service_type}\n"
            f"📊 <b>Holati:</b> {st_text}\n"
            f"💰 <b>Narxi:</b> {o.price:,.0f} SUM\n"
            f"📍 <b>Manzil:</b> {o.address}\n"
            f"📅 <b>Vaqt:</b> {created_str}\n"
        )
        if o.assigned_worker:
            msg += f"👷 <b>Usta:</b> {o.assigned_worker.first_name} (📞 <code>{o.assigned_worker.phone_number or 'Mavjud emas'}</code>)\n"

        await query.message.reply_html(msg)

    bottom_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("◀️ Orqaga (Buyurtmalarim)", callback_data="orders_nav_menu"),
            InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")
        ]
    ])
    await query.message.reply_html("<i>Boshqa bo'limga o'tish:</i>", reply_markup=bottom_markup)

async def orders_nav_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'orders_nav_menu':
        return await history_command(update, context)
    elif data == 'orders_nav_active':
        orders = await get_client_orders_filtered(query.from_user.id, 'ACTIVE')
        return await render_client_orders_list(query, orders, "🟣 JARAYONDAGI BUYURTMALARINGIZ")
    elif data == 'orders_nav_finished':
        orders = await get_client_orders_filtered(query.from_user.id, 'FINISHED')
        return await render_client_orders_list(query, orders, "🟢 YAKUNLANGAN BUYURTMALARINGIZ")
    elif data == 'orders_nav_all':
        orders = await get_client_orders_filtered(query.from_user.id, 'ALL')
        return await render_client_orders_list(query, orders, "📋 BARCHA BUYURTMALARINGIZ")

async def search_order_id_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cancel_kb = ReplyKeyboardMarkup([["❌ Bekor Qilish / Orqaga"]], resize_keyboard=True)
    await query.message.reply_html(
        "🔍 <b>Qidirmoqchi bo'lgan buyurtmangiz raqamini (ID) yozing:</b>\n"
        "<i>(Masalan: 12 yoki #12)</i>",
        reply_markup=cancel_kb
    )
    return SEARCH_ORDER_ID_STATE

async def search_order_id_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().replace('#', '')
    user = await get_or_create_client_user(update.effective_user)
    kb = get_client_keyboard(user)

    if text.startswith("❌") or "bekor" in text.lower() or "orqaga" in text.lower():
        await update.message.reply_text("Qidiruv bekor qilindi.", reply_markup=kb)
        return ConversationHandler.END

    if not text.isdigit():
        await update.message.reply_html("⚠️ Iltimos, faqat raqam kiriting (masalan: <b>15</b>).", reply_markup=kb)
        return ConversationHandler.END

    order = await get_order_by_numeric_id(text, update.effective_user.id)
    if not order:
        await update.message.reply_html(
            f"❌ <b>#{text}</b> raqamli buyurtmangiz topilmadi.\nIltimos, raqamni to'g'ri kiritganingizni tekshiring.",
            reply_markup=kb
        )
        return ConversationHandler.END

    status_map = {
        'PENDING': '🟡 Ochiq / Kutilmoqda',
        'DISPATCHED': '🔵 Usta Biriktirildi',
        'STARTED': '🟣 Ish Jarayonda',
        'FINISHED': '🟢 Yakunlangan',
        'CANCELLED': '🔴 Bekor Qilingan'
    }
    st_text = status_map.get(order.status, order.status)
    created_str = order.created_at.strftime("%d.%m.%Y %H:%M") if hasattr(order, 'created_at') and order.created_at else ''

    msg = (
        f"<b>🎯 TOPILGAN BUYURTMANGIZ: #{order.id}</b>\n\n"
        f"📌 <b>Nom:</b> {order.title}\n"
        f"📁 <b>Yo'nalish:</b> {order.service_type}\n"
        f"📊 <b>Holati:</b> {st_text}\n"
        f"💰 <b>Narxi:</b> {order.price:,.0f} SUM\n"
        f"📍 <b>Manzil:</b> {order.address}\n"
        f"📅 <b>Vaqt:</b> {created_str}\n"
    )
    if order.assigned_worker:
        msg += f"👷 <b>Usta:</b> {order.assigned_worker.first_name} (📞 <code>{order.assigned_worker.phone_number or ''}</code>)\n"

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ Orqaga (Buyurtmalarim)", callback_data="orders_nav_menu")],
        [InlineKeyboardButton("🏠 Bosh Menyu", callback_data="go_main_menu")]
    ])
    await update.message.reply_html(msg, reply_markup=markup)
    return ConversationHandler.END

async def callback_go_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = await get_or_create_client_user(query.from_user)
    kb = get_client_keyboard(user)
    try:
        await query.delete_message()
    except Exception:
        pass
    await query.message.reply_html("🏠 <b>Asosiy Bosh Menyu:</b>", reply_markup=kb)

async def cancel_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_client_user(update.effective_user)
    kb = get_client_keyboard(user)
    context.user_data.clear()
    await update.message.reply_html("❌ <b>Jarayon bekor qilindi.</b>", reply_markup=kb)
    return ConversationHandler.END

async def cancel_flow_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = await get_or_create_client_user(query.from_user)
    kb = get_client_keyboard(user)
    context.user_data.clear()
    await query.edit_message_text("❌ <b>Jarayon bekor qilindi.</b>", parse_mode='HTML')
    await query.message.reply_text("Bosh menyu:", reply_markup=kb)
    return ConversationHandler.END

# --- SETUP CLIENT BOT APPLICATION ---

def build_client_bot_application(token: str):
    if not token or not token.strip():
        return None

    app = ApplicationBuilder().token(token.strip()).build()

    job_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('(?i).*(buyurtma berish|ish joylash|buyurtma).*'), start_job_posting),
            CommandHandler('neworder', start_job_posting)
        ],
        states={
            CAT_SELECT: [
                CallbackQueryHandler(cat_selected, pattern='^cat_'),
                CallbackQueryHandler(cancel_flow_callback, pattern='^cancel_flow$')
            ],
            WORK_FORMAT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, work_format_selected),
                CallbackQueryHandler(work_format_selected, pattern='^fmt_'),
                CallbackQueryHandler(cancel_flow_callback, pattern='^cancel_flow$')
            ],
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, title_received)],
            DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, desc_received)],
            LOC_CHOICE: [
                MessageHandler(filters.LOCATION, loc_choice_or_direct_received),
                MessageHandler(filters.TEXT & ~filters.COMMAND, loc_choice_or_direct_received)
            ],
            LOCATION: [
                MessageHandler(filters.LOCATION, location_received),
                MessageHandler(filters.TEXT & ~filters.COMMAND, location_received)
            ],
            CONTACT: [
                MessageHandler(filters.CONTACT, contact_received),
                MessageHandler(filters.TEXT & ~filters.COMMAND, contact_received)
            ],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price_received)],
            CONFIRM: [
                CallbackQueryHandler(edit_field_cat_callback, pattern='^edit_field_cat$'),
                CallbackQueryHandler(set_field_cat_callback, pattern='^set_field_cat_'),
                CallbackQueryHandler(cancel_flow_callback, pattern='^cancel_flow$'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_job)
            ],
            EDIT_JOB_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, title_edited_in_confirm)],
            EDIT_JOB_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, desc_edited_in_confirm)],
            EDIT_JOB_LOC: [
                MessageHandler(filters.LOCATION, loc_edited_in_confirm),
                MessageHandler(filters.TEXT & ~filters.COMMAND, loc_edited_in_confirm)
            ],
            EDIT_JOB_PHONE: [
                MessageHandler(filters.CONTACT, phone_edited_in_confirm),
                MessageHandler(filters.TEXT & ~filters.COMMAND, phone_edited_in_confirm)
            ],
            EDIT_JOB_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price_edited_in_confirm)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_flow),
            MessageHandler(filters.Regex('(?i).*(bekor|cancel|chiqish|orqaga|❌).*'), cancel_flow),
            CallbackQueryHandler(cancel_flow_callback, pattern='^cancel_flow$')
        ],
        allow_reentry=True
    )

    edit_name_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_name_callback, pattern='^edit_profile_name$')],
        states={
            EDIT_NAME_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_edited_received)]
        },
        fallbacks=[CommandHandler('cancel', cancel_flow), MessageHandler(filters.Regex('^❌'), cancel_flow)],
        allow_reentry=True
    )

    edit_phone_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_phone_callback, pattern='^edit_profile_phone$')],
        states={
            EDIT_PHONE_STATE: [MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), phone_edited_received)]
        },
        fallbacks=[CommandHandler('cancel', cancel_flow), MessageHandler(filters.Regex('^❌'), cancel_flow)],
        allow_reentry=True
    )

    search_order_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(search_order_id_start, pattern='^orders_nav_search$')],
        states={
            SEARCH_ORDER_ID_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_order_id_received)]
        },
        fallbacks=[CommandHandler('cancel', cancel_flow), MessageHandler(filters.Regex('^❌'), cancel_flow)],
        allow_reentry=True
    )

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('profile', profile_command))
    app.add_handler(CommandHandler('credits', credits_command))

    app.add_handler(job_handler)
    app.add_handler(edit_name_handler)
    app.add_handler(edit_phone_handler)
    app.add_handler(search_order_handler)

    app.add_handler(CallbackQueryHandler(cancel_flow_callback, pattern='^cancel_flow$'))
    app.add_handler(CallbackQueryHandler(orders_nav_callback, pattern='^orders_nav_'))
    app.add_handler(CallbackQueryHandler(callback_go_main_menu, pattern='^go_main_menu$'))
    app.add_handler(CallbackQueryHandler(profile_command, pattern='^go_profile$'))
    app.add_handler(CallbackQueryHandler(credits_command, pattern='^go_credits$'))

    app.add_handler(MessageHandler(filters.Regex("(?i).*(profil|shaxsiy).*"), profile_command))
    app.add_handler(MessageHandler(filters.Regex("(?i).*(kredit|balans).*"), credits_command))
    app.add_handler(MessageHandler(filters.Regex("(?i).*(buyurtmalarim|tarix).*"), history_command))
    app.add_handler(MessageHandler(filters.Regex("(?i).*(call center|aloqa).*"), help_command))
    app.add_handler(MessageHandler(filters.Regex("(?i).*(haqimizda|ma'lumot|yordam).*"), help_command))

    return app
