import asyncio
import logging
from django.core.management.base import BaseCommand
from telegram_bot.runner import run_dual_bots

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs the Full-Xizmat Dual Telegram Bots (Client/Employer Bot & Worker/Master Bot)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='all',
            choices=['all', 'client', 'worker'],
            help='Specify which bot to run: all (default), client, or worker'
        )

    def handle(self, *args, **options):
        bot_type = options.get('type', 'all')
        self.stdout.write(self.style.SUCCESS(f"Starting Full-Xizmat Telegram Bot Supervisor (mode: {bot_type})..."))
        try:
            asyncio.run(run_dual_bots(bot_type=bot_type))
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Bot supervisor stopped by user."))

