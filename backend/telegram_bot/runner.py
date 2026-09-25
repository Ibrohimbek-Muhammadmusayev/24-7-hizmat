import asyncio
import logging
from asgiref.sync import sync_to_async
from django.conf import settings
from bot_control.models import BotConfig
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
from telegram_bot.texts import t
from telegram_bot.bot import build_bot_application, get_all_registered_users_for_notification
from telegram_client_bot.bot import build_client_bot_application, get_all_client_users_for_notification
from telegram_client_bot.texts import t as client_t

logger = logging.getLogger(__name__)

async def broadcast_restart_notification(bot):
    """Worker bot qayta ishga tushganda barcha ustalarga xavfsiz xabar yuborish"""
    try:
        await asyncio.sleep(2)
        users = await get_all_registered_users_for_notification()
        if not users:
            return

        logger.info(f"Worker bot restart xabarnomasi {len(users)} ta foydalanuvchiga yuborilmoqda...")
        sent_count = 0
        for u in users:
            tg_id = u['telegram_id']
            lang = u.get('language') or 'uz'
            
            text = t('bot_restarted_notification', lang)
            keyboard = [
                [InlineKeyboardButton(t('btn_restart_bot', lang), callback_data="reset_to_main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await bot.send_message(
                    chat_id=tg_id,
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
                sent_count += 1
            except TelegramError as te:
                logger.warning(f"User {tg_id} ga restart xabarnomasi yuborilmadi: {te}")
            except Exception as ex:
                logger.error(f"User {tg_id} ga xabar yuborishda xatolik: {ex}")
                
            await asyncio.sleep(0.08)

        logger.info(f"Worker restart xabarnomasi yakunlandi. Yuborildi: {sent_count}/{len(users)}")
    except Exception as e:
        logger.error(f"Worker restart xabarnomasini yuborishda xatolik: {e}")

async def broadcast_client_restart_notification(bot):
    """Client (Ish joylash) boti qayta ishga tushganda barcha ish beruvchilarga xavfsiz xabar yuborish"""
    try:
        await asyncio.sleep(2)
        users = await get_all_client_users_for_notification()
        if not users:
            return

        logger.info(f"Client bot restart xabarnomasi {len(users)} ta foydalanuvchiga yuborilmoqda...")
        sent_count = 0
        for u in users:
            tg_id = u['telegram_id']
            lang = u.get('language') or 'uz'
            
            text = client_t('bot_restarted_notification', lang)
            keyboard = [
                [InlineKeyboardButton(client_t('btn_restart_bot', lang), callback_data="reset_to_main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await bot.send_message(
                    chat_id=tg_id,
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
                sent_count += 1
            except TelegramError as te:
                logger.warning(f"Client user {tg_id} ga restart xabari yuborilmadi: {te}")
            except Exception as ex:
                logger.error(f"Client user {tg_id} ga xabar yuborishda xatolik: {ex}")
                
            await asyncio.sleep(0.08)

        logger.info(f"Client restart xabarnomasi yakunlandi. Yuborildi: {sent_count}/{len(users)}")
    except Exception as e:
        logger.error(f"Client restart xabarnomasini yuborishda xatolik: {e}")

async def run_dual_bots(bot_type='all'):
    config = await sync_to_async(BotConfig.get_config)()
    worker_token = (config.worker_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')).strip()
    client_token = (config.client_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')).strip()

    running_apps = []

    # 1. Worker bot (24/7-ishlar)
    if bot_type in ['all', 'worker'] and worker_token and worker_token != '7890123456:AAExampleBotTokenPlaceholder':
        try:
            worker_app = build_bot_application(worker_token)
            logger.info("🛠️ 24/7-ishlar (Worker) boti ishga tushirilmoqda...")
            await worker_app.initialize()
            await worker_app.start()
            await worker_app.updater.start_polling(drop_pending_updates=True)
            logger.info("🛠️ 24/7-ishlar boti muvaffaqiyatli ishga tushdi.")
            running_apps.append(worker_app)
            asyncio.create_task(broadcast_restart_notification(worker_app.bot))
        except Exception as e:
            logger.error(f"Worker botini ishga tushirishda xatolik: {e}")

    # 2. Client bot (Ish Joylash Boti)
    if bot_type in ['all', 'client'] and client_token and client_token != '7890123456:AAExampleBotTokenPlaceholder' and client_token != worker_token:
        try:
            client_app = build_client_bot_application(client_token)
            logger.info("📢 Ish Joylash (Client) boti ishga tushirilmoqda...")
            await client_app.initialize()
            await client_app.start()
            await client_app.updater.start_polling(drop_pending_updates=True)
            logger.info("📢 Ish Joylash boti muvaffaqiyatli ishga tushdi.")
            running_apps.append(client_app)
            asyncio.create_task(broadcast_client_restart_notification(client_app.bot))
        except Exception as e:
            logger.error(f"Client botini ishga tushirishda xatolik: {e}")
    elif client_token == worker_token and bot_type == 'client':
        try:
            client_app = build_client_bot_application(client_token)
            logger.info("📢 Ish Joylash (Client) boti ishga tushirilmoqda...")
            await client_app.initialize()
            await client_app.start()
            await client_app.updater.start_polling(drop_pending_updates=True)
            logger.info("📢 Ish Joylash boti muvaffaqiyatli ishga tushdi.")
            running_apps.append(client_app)
            asyncio.create_task(broadcast_client_restart_notification(client_app.bot))
        except Exception as e:
            logger.error(f"Client botini ishga tushirishda xatolik: {e}")

    if not running_apps:
        logger.warning("Ishga tushirish uchun hech qanday faol bot topilmadi yoki tokenlar noto'g'ri.")
        return

    stop_event = asyncio.Event()
    try:
        await stop_event.wait()
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Botlar to'xtatilmoqda...")
    finally:
        for app in running_apps:
            if app.updater and app.updater.running:
                await app.updater.stop()
            if app.running:
                await app.stop()
            await app.shutdown()
        logger.info("Barcha botlar to'xtatildi.")


