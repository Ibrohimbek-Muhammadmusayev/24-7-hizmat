from django.db import models
from django.conf import settings

class BotConfig(models.Model):
    # Backward compatibility token
    token = models.CharField(max_length=255, blank=True, default='')

    # Dual Bot Tokens
    client_bot_token = models.CharField(max_length=255, blank=True, default='') # Ish beruvchilar / Mijozlar boti
    worker_bot_token = models.CharField(max_length=255, blank=True, default='') # Ishchilar / Ustalar boti

    is_running = models.BooleanField(default=False)
    pid = models.IntegerField(null=True, blank=True)
    last_started_at = models.DateTimeField(null=True, blank=True)

    # Monetization & Credit System
    monetization_enabled = models.BooleanField(default=False) # False = Bepul, True = Kredit tizimi
    initial_free_credits = models.IntegerField(default=3)      # Yangi foydalanuvchiga beriladigan bepul kredit
    job_posting_cost_credits = models.IntegerField(default=1)  # 1 ta ish joylash narxi (kreditda)
    credit_price_sum = models.DecimalField(max_digits=12, decimal_places=2, default=10000.0) # 1 kredit narxi (so'mda)
    
    # Platform & Brand Identity
    project_name = models.CharField(max_length=150, blank=True, default="IshBazari", verbose_name="Loyiha (Brend) nomi")

    # CMS & Dynamic Bot Content Settings
    welcome_text = models.TextField(
        blank=True, 
        default="Assalomu alaykum, {first_name}! 👋\n\n{project_name} usta va ishlar platformasining rasmiy botiga xush kelibsiz!\n\nQuyidagi menyu orqali kerakli bo'limni tanlang:"
    )
    welcome_image_url = models.CharField(max_length=500, blank=True, default='')
    about_text = models.TextField(
        blank=True, 
        default="{project_name} — O'zbekiston bo'ylab usta va mijozlarni tezkor bog'lovchi yagona professional xizmat platformasi.\n\nIshonchli ustalar, kafolatlangan xizmat va shaffof narxlar!"
    )
    call_center_phone = models.CharField(max_length=50, blank=True, default="+998 (71) 200-00-00")
    help_text = models.TextField(
        blank=True, 
        default="• Buyurtma Berish: Kerakli xizmat turini tanlab, oson buyurtma qoldiring.\n• Ish Qidirish: Ustalar yangi buyurtmalarni qabul qilishi mumkin.\n• Profilim: Ma'lumotlaringizni ko'ring va tahrirlang.\n• Buyurtmalarim: Buyurtmalar holatini kuzatib boring."
    )

    # Custom Bot Links
    client_bot_url = models.CharField(max_length=500, blank=True, default='', verbose_name="Ish beruvchi bot havolasi")
    worker_bot_url = models.CharField(max_length=500, blank=True, default='', verbose_name="Usta bot havolasi")

    # Ilovaga kirish (Web App URL)
    app_url = models.CharField(max_length=500, blank=True, default='', verbose_name="Ilova havolasi (URL)")
    app_url_enabled = models.BooleanField(default=False, verbose_name="Ilovaga kirish tugmasi faolmi")

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"BotConfig (running={self.is_running}, pid={self.pid}, monetization={self.monetization_enabled})"

    @classmethod
    def get_config(cls):
        config, created = cls.objects.get_or_create(id=1)
        # Migrate or sync default tokens if empty or placeholder
        default_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if default_token and (not config.token or config.token == '7890123456:AAExampleBotTokenPlaceholder'):
            config.token = default_token
        
        if config.token and config.token != '7890123456:AAExampleBotTokenPlaceholder':
            if not config.client_bot_token or config.client_bot_token == '7890123456:AAExampleBotTokenPlaceholder':
                config.client_bot_token = config.token
                config.save()
        elif default_token:
            if not config.client_bot_token or config.client_bot_token == '7890123456:AAExampleBotTokenPlaceholder':
                config.client_bot_token = default_token
                config.save()
        return config

    @classmethod
    def get_project_name(cls):
        """Loyiha / Brend nomini qaytaradi (masalan: IshBazari)"""
        try:
            config = cls.get_config()
            if config.project_name and config.project_name.strip():
                return config.project_name.strip()
        except Exception:
            pass
        return "IshBazari"

    @classmethod
    def get_client_bot_link(cls):
        """
        Ish beruvchilar (Mijozlar) botiga o'tish havolasini qaytaradi.
        1. Agar admin panelda client_bot_url ko'rsatilgan bo'lsa, o'shani oladi.
        2. Aks holda client_bot_token orqali Telegram API'dan bot username'ini aniqlaydi.
        3. Standart holatda fallback havola qaytaradi.
        """
        try:
            config = cls.get_config()
            if config.client_bot_url and config.client_bot_url.strip():
                return config.client_bot_url.strip()

            token = config.client_bot_token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
            if token and token != '7890123456:AAExampleBotTokenPlaceholder':
                import json
                import ssl
                import urllib.request
                try:
                    ctx = ssl._create_unverified_context()
                    req = urllib.request.Request(f"https://api.telegram.org/bot{str(token).strip()}/getMe", headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, context=ctx, timeout=3) as response:
                        data = json.loads(response.read().decode('utf-8'))
                        if data.get('ok') and data.get('result', {}).get('username'):
                            uname = data['result']['username']
                            return f"https://t.me/{uname}?start=ref_worker_bot"
                except Exception:
                    pass
        except Exception:
            pass
        return "https://t.me/ishjoyla_bot?start=ref_worker_bot"

    @classmethod
    def get_worker_bot_link(cls):
        """
        Usta va ish izlovchilar botiga o'tish havolasini qaytaradi.
        """
        try:
            config = cls.get_config()
            if config.worker_bot_url and config.worker_bot_url.strip():
                return config.worker_bot_url.strip()

            token = config.worker_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
            if token and token != '7890123456:AAExampleBotTokenPlaceholder':
                import json
                import ssl
                import urllib.request
                try:
                    ctx = ssl._create_unverified_context()
                    req = urllib.request.Request(f"https://api.telegram.org/bot{str(token).strip()}/getMe", headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, context=ctx, timeout=3) as response:
                        data = json.loads(response.read().decode('utf-8'))
                        if data.get('ok') and data.get('result', {}).get('username'):
                            uname = data['result']['username']
                            return f"https://t.me/{uname}?start=ref_client_bot"
                except Exception:
                    pass
        except Exception:
            pass
        return "https://t.me/ish_24_7_bot?start=ref_client_bot"
