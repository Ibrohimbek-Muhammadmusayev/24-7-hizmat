import os
import sys
from django.apps import AppConfig

class BotControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_control'
    verbose_name = 'Telegram Bot Control'

    def ready(self):
        # Prevent double execution with Django auto-reloader
        if os.environ.get('RUN_MAIN') == 'true' or 'runserver' not in sys.argv:
            # Only start when running server / Daphne / Gunicorn
            is_server = any(cmd in sys.argv for cmd in ['runserver', 'daphne', 'gunicorn', 'uvicorn']) or os.environ.get('SERVER_SOFTWARE')
            if is_server or os.environ.get('RUN_MAIN') == 'true':
                try:
                    from .views import spawn_bot_process, is_pid_running
                    from .models import BotConfig
                    
                    config = BotConfig.get_config()
                    if not config.pid or not is_pid_running(config.pid):
                        pid = spawn_bot_process()
                        config.is_running = True
                        config.pid = pid
                        config.save(update_fields=['is_running', 'pid'])
                        print(f"[AUTO-START] Telegram Botlar avtomatik ishga tushirildi! (PID: {pid})")
                except Exception as e:
                    print("[AUTO-START WARNING] Botni avtomatik ishga tushirishda xatolik:", e)

