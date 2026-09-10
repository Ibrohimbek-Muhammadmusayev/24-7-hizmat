import logging
import asyncio
import math
from asgiref.sync import sync_to_async
from django.conf import settings
from django.db.models import Q
from accounts.models import User
from bot_control.models import BotConfig
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError

logger = logging.getLogger(__name__)

def calculate_distance_km(lat1, lon1, lat2, lon2):
    try:
        r = 6371.0 # Yer radiusi km
        dlat = math.radians(float(lat2) - float(lat1))
        dlon = math.radians(float(lon2) - float(lon1))
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(float(lat1)))
            * math.cos(math.radians(float(lat2)))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c
    except Exception:
        return 99999.0

async def notify_matching_workers_about_job(job_post_id):
    """
    Yangi e'lon berilganda:
    1. Soha/mutaxassislik bo'yicha mos keladigan va shu viloyat/tuman/shahardagi barcha faol ishchilarga.
    2. Sohasidan qat'i nazar, agar ish joylashuvidan 5 km radiusda bo'lsa (GPS bo'yicha) — o'sha yaqin atrofdagi barcha ishchilarga.
    3. 5 km dan uzoq va sohasi to'g'ri kelmaydiganlarga bormaydi.
    """
    from orders.models import JobPost
    
    try:
        job = await sync_to_async(
            lambda: JobPost.objects.select_related('category', 'position', 'region', 'employer').get(id=job_post_id)
        )()
    except Exception as e:
        logger.error(f"JobPost #{job_post_id} topilmadi: {e}")
        return

    # Worker bot tokenni olish
    config = await sync_to_async(BotConfig.get_config)()
    worker_bot_token = (config.worker_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')).strip()
    
    if not worker_bot_token or worker_bot_token == '7890123456:AAExampleBotTokenPlaceholder':
        logger.warning("Ishchilarga xabarnoma yuborish uchun Worker bot token mavjud emas.")
        return

    def get_target_workers():
        # Faqat ro'yxatdan o'tgan, telegram_id si bor, band bo'lmagan va bildirishnomani o'chirmagan ishchilar
        base_qs = User.objects.filter(
            role=User.Role.WORKER, 
            telegram_id__isnull=False, 
            is_registered=True,
            is_busy=False
        ).exclude(notification_setting='off').prefetch_related('selected_positions')

        matched_worker_ids = set()

        # 1. Mutaxassislik / Soha bo'yicha mos va bir xil hududdagi ishchilar
        cat_pos_filter = Q()
        if job.position_id:
            cat_pos_filter |= Q(selected_positions__id=job.position_id) | Q(position_id=job.position_id)
        if job.category_id:
            cat_pos_filter |= Q(category_id=job.category_id)

        if cat_pos_filter:
            spec_workers = base_qs.filter(cat_pos_filter)
            # Hudud bo'yicha tekshirish (shu viloyat yoki tuman bo'lsa)
            if job.region_id:
                spec_workers = spec_workers.filter(
                    Q(region_id=job.region_id) | 
                    Q(district__iexact=job.district) if job.district else Q(region_id=job.region_id)
                )
            elif job.district:
                spec_workers = spec_workers.filter(district__icontains=job.district)

            for w in spec_workers.distinct()[:50]:
                matched_worker_ids.add(w.id)

        # 2. 5 km RADIUSDAGI BARCHA ISHCHILAR (Sohasidan qat'i nazar!)
        if job.latitude and job.longitude:
            # GPS koordinatasi mavjud bo'lgan barcha ishchilarni tekshirish
            gps_workers = base_qs.filter(latitude__isnull=False, longitude__isnull=False)
            for w in gps_workers:
                dist = calculate_distance_km(job.latitude, job.longitude, w.latitude, w.longitude)
                if dist <= 5.0: # 5 km atrofida
                    matched_worker_ids.add(w.id)

        if not matched_worker_ids:
            return []

        return list(User.objects.filter(id__in=matched_worker_ids))

    target_workers = await sync_to_async(get_target_workers)()
    if not target_workers:
        logger.info(f"JobPost #{job_post_id} uchun mos/yaqin ishchilar topilmadi.")
        return

    bot = Bot(token=worker_bot_token)
    sent_count = 0

    pos_name = job.position.name_uz if job.position else (job.custom_position_name or (job.category.name_uz if job.category else "Xizmat"))
    emp_type_text = "⚡️ Kunbay / Bir martalik" if job.employment_type == 'daily' else "💼 Doimiy ish"
    price_text = f"💰 {job.price_amount}" if (not job.is_price_negotiable and job.price_amount) else "🤝 Kelishilgan narxda"

    loc_str = ""
    if job.region:
        loc_str += job.region.name_uz
    if job.district:
        loc_str += f", {job.district}"
    if not loc_str:
        loc_str = "Ko'rsatilmagan"
    from orders.models import JobApplication

    @sync_to_async
    def record_job_invite(w_id, j_id):
        try:
            app, created = JobApplication.objects.get_or_create(
                job_post_id=j_id,
                worker_id=w_id,
                defaults={'is_invited': True, 'status': JobApplication.Status.PENDING}
            )
            if not created and app.is_deleted_by_worker:
                # Agar oldin o'chirgan bo'lsa ham yangi bildirishnoma kelganda taklif sifatida ko'rsatish
                pass
        except Exception as e:
            logger.error(f"Error recording job invite: {e}")

    for worker in target_workers:
        dist_note = ""
        if job.latitude and job.longitude and worker.latitude and worker.longitude:
            d = calculate_distance_km(job.latitude, job.longitude, worker.latitude, worker.longitude)
            if d <= 5.0:
                dist_note = f"📍 <b>Masofa:</b> ~{d:.1f} km (Sizga juda yaqin!)\n"
            else:
                dist_note = f"📍 <b>Masofa:</b> ~{d:.1f} km\n"

        # Ishchilar soni va jinsi bo'yicha aniq, tushunarli matn
        gender_req = job.gender_requirement
        if gender_req == 'male':
            gender_txt = "Faqat erkak ishchi"
        elif gender_req == 'female':
            gender_txt = "Faqat ayol ishchi"
        else:
            gender_txt = "Jinsi: Farqi yo'q (Erkak/Ayol)"

        msg_text = (
            f"🚨 <b>YANGI ISH BUYURTMASI!</b>\n\n"
            f"📋 <b>Soha:</b> {pos_name} ({emp_type_text})\n"
            f"📍 <b>Hudud:</b> {loc_str}\n"
            f"{dist_note}"
            f"👥 <b>Kerakli ishchilar:</b> {job.workers_count} ({gender_txt})\n"
            f"⏱ <b>Vaqt:</b> {job.get_start_time_type_display()}\n"
            f"💵 <b>To'lov:</b> {price_text}\n"
            f"📝 <b>Tavsif:</b> {job.description[:150] if job.description else 'Tavsif berilmagan'}...\n\n"
            f"<i>Batafsil ma'lumot olish va ishni qabul qilish uchun quyidagi tugmani bosing:</i>"
        )

        keyboard = [
            [InlineKeyboardButton("💼 Ishni ko'rish va topshirish", callback_data=f"view_job_{job.id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await bot.send_message(
                chat_id=worker.telegram_id,
                text=msg_text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            sent_count += 1
            # Ishchining "So'rovlar / Takliflar" ro'yxatida ko'rinishi uchun taklif sifatida saqlab qo'yamiz
            await record_job_invite(worker.id, job.id)
            await asyncio.sleep(0.08)
        except TelegramError as te:
            logger.warning(f"Worker {worker.telegram_id} ga bildirishnoma bormadi: {te}")
        except Exception as ex:
            logger.error(f"Xatolik: {ex}")

    logger.info(f"JobPost #{job_post_id} e'loni bo'yicha {sent_count} ta ishchiga push-xabar yetkazildi.")
