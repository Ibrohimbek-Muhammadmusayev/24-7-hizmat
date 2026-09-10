import asyncio
import logging
from asgiref.sync import sync_to_async
from django.conf import settings
from bot_control.models import BotConfig
from telegram_client_bot.bot import build_client_bot_application

logger = logging.getLogger(__name__)

async def run_client_bot():
    config = await sync_to_async(BotConfig.get_config)()
    token = (config.client_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')).strip()

    if not token or token == '7890123456:AAExampleBotTokenPlaceholder':
        logger.warning("Ish joylash boti tokeni kiritilmagan. Dashboard orqali tokenni kiriting.")
        return

    try:
        app = build_client_bot_application(token)
        logger.info("Ish joylash boti (Job Post Enterprise Bot) ishga tushirilmoqda...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        logger.info("Ish joylash boti muvaffaqiyatli ishga tushdi va xabarlarni qabul qilmoqda.")

        stop_event = asyncio.Event()
        try:
            await stop_event.wait()
        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("Ish joylash boti to'xtatilmoqda...")
        finally:
            if app.updater and app.updater.running:
                await app.updater.stop()
            if app.running:
                await app.stop()
            await app.shutdown()
            logger.info("Ish joylash boti to'xtatildi.")
    except Exception as e:
        logger.error(f"Ish joylash botini ishga tushirishda xatolik: {e}")
