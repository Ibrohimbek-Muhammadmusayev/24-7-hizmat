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
    
    # CMS & Dynamic Bot Content Settings
    welcome_text = models.TextField(
        blank=True, 
        default="Assalomu alaykum, {first_name}! 👋\n\n24/7-ishlar usta va ishlar platformasining rasmiy botiga xush kelibsiz!\n\nQuyidagi menyu orqali kerakli bo'limni tanlang:"
    )
    welcome_image_url = models.CharField(max_length=500, blank=True, default='')
    about_text = models.TextField(
        blank=True, 
        default="24/7-ishlar — O'zbekiston bo'ylab usta va mijozlarni tezkor bog'lovchi yagona professional xizmat platformasi.\n\nIshonchli ustalar, kafolatlangan xizmat va shaffof narxlar!"
    )
    call_center_phone = models.CharField(max_length=50, blank=True, default="+998 (71) 200-00-00")
    help_text = models.TextField(
        blank=True, 
        default="• Buyurtma Berish: Kerakli xizmat turini tanlab, oson buyurtma qoldiring.\n• Ish Qidirish: Ustalar yangi buyurtmalarni qabul qilishi mumkin.\n• Profilim: Ma'lumotlaringizni ko'ring va tahrirlang.\n• Buyurtmalarim: Buyurtmalar holatini kuzatib boring."
    )

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
