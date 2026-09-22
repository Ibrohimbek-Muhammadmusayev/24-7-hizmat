from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CALL_CENTER = 'CALL_CENTER', 'Call Center Operator'
        WORKER = 'WORKER', 'Ish qidiruvchi / Usta / Xodim'
        CLIENT = 'CLIENT', 'Ish beruvchi / Mijoz'

    class Language(models.TextChoices):
        UZ_LATIN = 'uz', "O'zbekcha (Lotin)"
        UZ_CYRILLIC = 'oz', "Ўзбекча (Кирилл)"
        RUSSIAN = 'ru', "Русский"
        ENGLISH = 'en', "English"

    class Gender(models.TextChoices):
        MALE = 'male', "Erkak"
        FEMALE = 'female', "Ayol"

    class EmploymentType(models.TextChoices):
        DAILY = 'daily', "Bir martalik / Kunbay"
        PERMANENT = 'permanent', "Doimiy ish"
        BOTH = 'both', "Ikkalasi ham"

    class WorkSchedule(models.TextChoices):
        DAY_SHIFT = 'day_shift', "09:00 - 18:00 (Kunduzgi)"
        FULL_TIME_24_7 = '24_7', "24/7 (Istalgan vaqtda / Shoshilinch)"
        FLEXIBLE = 'flexible', "Erkin grafik"

    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.WORKER)
    language = models.CharField(max_length=10, choices=Language.choices, default=Language.UZ_LATIN, verbose_name="Til")
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    
    # 1-Qadam: Shaxsiy ma'lumotlar
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True, blank=True, verbose_name="Jinsi")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Yoshi")

    # 2-Qadam: Manzil va Hudud
    region = models.ForeignKey(
        'locations.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Viloyat / Hudud"
    )
    district = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tuman / Shahar")
    street_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mahalla, ko'cha, uy raqami")
    
    # GPS Joylashuv (Location)
    latitude = models.FloatField(null=True, blank=True, verbose_name="GPS Kenglik (Latitude)")
    longitude = models.FloatField(null=True, blank=True, verbose_name="GPS Uzunlik (Longitude)")
    address_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Aniq manzil / Joylashuv matni")

    # 3-Qadam: Soha va Mutaxassisliklar (10 tagacha)
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workers',
        verbose_name="Soha / Yo'nalish"
    )
    position = models.ForeignKey(
        'categories.Position',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='workers',
        verbose_name="Lavozim / Mutaxassislik"
    )
    selected_positions = models.ManyToManyField(
        'categories.Position',
        blank=True,
        related_name='selected_by_workers',
        verbose_name="Tanlangan lavozimlar (10 tagacha)"
    )

    # Agar "Boshqa" (Custom) kiritilgan bo'lsa
    custom_category = models.CharField(max_length=255, blank=True, null=True, verbose_name="Boshqa soha (qo'lda kiritilgan)")
    custom_position = models.CharField(max_length=255, blank=True, null=True, verbose_name="Boshqa lavozim (qo'lda kiritilgan)")

    class NotificationSetting(models.TextChoices):
        ALL = 'all', "Barcha xabarlar yoqiq"
        NIGHT_MUTE = 'night_mute', "Tungi rejim (22:00 dan keyin ovozsiz)"
        OFF = 'off', "Bildirishnomalarni butunlay o'chirish"

    # 4-Qadam: Ish rejimi va Shartlari
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, default=EmploymentType.BOTH, verbose_name="Bandlik turi")
    work_schedule = models.CharField(max_length=20, choices=WorkSchedule.choices, default=WorkSchedule.FLEXIBLE, verbose_name="Ish vaqti rejimi")

    is_online = models.BooleanField(default=True)
    is_busy = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False, verbose_name="Ro'yxatdan to'liq o'tganmi")
    notification_setting = models.CharField(
        max_length=20, 
        choices=NotificationSetting.choices, 
        default=NotificationSetting.ALL,
        verbose_name="Bildirishnoma sozlamasi"
    )

    specialty = models.CharField(max_length=100, blank=True, null=True) # e.g. Santexnik, Elektrik
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(default=5.0)
    completed_jobs_count = models.PositiveIntegerField(default=0, verbose_name="Bajarilgan ishlar soni")

    # Job Posting Credits (Employer / Client Bot)
    job_credits = models.IntegerField(default=3)

    # Dual Bot Tracking
    started_client_bot = models.BooleanField(default=False)
    started_worker_bot = models.BooleanField(default=False)

    # Admin profile verification and mandatory update request
    needs_profile_update = models.BooleanField(default=False, verbose_name="Qayta to'ldirish talab qilinadimi")
    profile_update_reason = models.TextField(blank=True, null=True, verbose_name="Qayta to'ldirish sababi / Admin izohi")
    profile_update_fields = models.CharField(max_length=255, blank=True, null=True, verbose_name="Qayta to'ldirilishi kerak bo'lgan maydonlar (vergul bilan)")

    def __str__(self):
        return f"{self.first_name or self.username} ({self.phone_number or self.telegram_id}) - {self.get_role_display()}"


class WorkerPortfolio(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_items')
    file_id = models.CharField(max_length=255, verbose_name="Telegram File ID")
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="Rasm tavsifi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usta portfolio rasmi"
        verbose_name_plural = "Usta portfolio rasmlari"
        ordering = ['-created_at']


class WorkerReview(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    client_name = models.CharField(max_length=150, verbose_name="Mijoz ismi")
    client_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mijoz telefoni")
    rating = models.PositiveIntegerField(default=5, verbose_name="Baho (1-5)")
    comment = models.TextField(verbose_name="Sharh matni")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usta sharhi"
        verbose_name_plural = "Usta sharhlari"
        ordering = ['-created_at']


class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    message = models.TextField(verbose_name="Taklif / Shikoyat matni")
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Foydalanuvchi taklif/shikoyati"
        verbose_name_plural = "Foydalanuvchi taklif va shikoyatlari"
        ordering = ['-created_at']

