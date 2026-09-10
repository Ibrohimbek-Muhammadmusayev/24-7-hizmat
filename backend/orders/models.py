from django.db import models
from django.conf import settings

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Kutilmoqda'
        DISPATCHED = 'DISPATCHED', 'Ishchiga biriktirildi'
        STARTED = 'STARTED', 'Boshlandi / Yo\'lda'
        FINISHED = 'FINISHED', 'Yakunlandi'
        CANCELLED = 'CANCELLED', 'Bekor qilindi'

    class Source(models.TextChoices):
        TELEGRAM_BOT = 'TELEGRAM_BOT', 'Telegram Bot'
        CALL_CENTER = 'CALL_CENTER', 'Call Center'

    class WorkFormat(models.TextChoices):
        OFFLINE = 'OFFLINE', 'Joyiga borish (Offline)'
        ONLINE = 'ONLINE', 'Masofaviy (Online)'

    source = models.CharField(max_length=30, choices=Source.choices, default=Source.CALL_CENTER)
    work_format = models.CharField(max_length=20, choices=WorkFormat.choices, default=WorkFormat.OFFLINE)
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    title = models.CharField(max_length=255, default='Ish xizmati')
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=30)
    customer_telegram_id = models.BigIntegerField(null=True, blank=True)
    
    address = models.TextField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    service_type = models.CharField(max_length=100) # e.g. Santexnik, Elektrik
    description = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    assigned_worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_orders'
    )
    
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} [{self.source}] ({self.work_format}) - {self.title} ({self.status})"


class JobPost(models.Model):
    class EmploymentType(models.TextChoices):
        DAILY = 'daily', "Bir martalik / Kunbay"
        PERMANENT = 'permanent', "Doimiy ish (oylik)"

    class GenderRequirement(models.TextChoices):
        ANY = 'any', "Farqi yo'q"
        MALE = 'male', "Faqat erkak"
        FEMALE = 'female', "Faqat ayol"

    class Status(models.TextChoices):
        ACTIVE = 'active', "Faol / Qidirilmoqda"
        PAUSED = 'paused', "Vaqtincha to'xtatilgan"
        COMPLETED = 'completed', "Ishchi topildi / Yopilgan"
        CANCELLED = 'cancelled', "Bekor qilingan"

    class StartTimeType(models.TextChoices):
        URGENT = 'urgent', "Tezda (Bugun / Shoshilinch)"
        TOMORROW = 'tomorrow', "Ertaga"
        CUSTOM = 'custom', "Aniq sana / Kelishilgan"

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_job_posts',
        verbose_name="Ish beruvchi"
    )
    employment_type = models.CharField(
        max_length=20, 
        choices=EmploymentType.choices, 
        default=EmploymentType.DAILY,
        verbose_name="Bandlik turi"
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='job_posts',
        verbose_name="Asosiy soha"
    )
    position = models.ForeignKey(
        'categories.Position',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='job_posts',
        verbose_name="Mutaxassislik / Lavozim"
    )
    custom_position_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Boshqa mutaxassislik nomi")
    
    description = models.TextField(verbose_name="Ish tavsifi va sharoiti")
    photo_file_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Obyekt rasmi (Telegram File ID)")
    
    workers_count = models.CharField(max_length=50, default="1 nafar", verbose_name="Kerakli ishchilar soni")
    gender_requirement = models.CharField(
        max_length=20,
        choices=GenderRequirement.choices,
        default=GenderRequirement.ANY,
        verbose_name="Jinsi talabi"
    )
    
    start_time_type = models.CharField(
        max_length=20,
        choices=StartTimeType.choices,
        default=StartTimeType.URGENT,
        verbose_name="Boshlanish vaqti turi"
    )
    custom_start_date = models.CharField(max_length=100, blank=True, null=True, verbose_name="Aniq boshlanish sanasi/vaqti")
    
    is_price_negotiable = models.BooleanField(default=True, verbose_name="Narxi kelishilganmi")
    price_amount = models.CharField(max_length=100, blank=True, null=True, verbose_name="To'lov summasi")
    
    region = models.ForeignKey(
        'locations.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='job_posts',
        verbose_name="Viloyat"
    )
    district = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tuman / Shahar")
    address = models.TextField(blank=True, null=True, verbose_name="Aniq manzil / Mo'ljal")
    latitude = models.FloatField(blank=True, null=True, verbose_name="GPS Kenglik")
    longitude = models.FloatField(blank=True, null=True, verbose_name="GPS Uzunlik")
    
    contact_name = models.CharField(max_length=150, verbose_name="Aloqa uchun ism")
    contact_phone = models.CharField(max_length=50, verbose_name="Aloqa telefoni")
    contact_telegram_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Aloqa Telegram Username")
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="E'lon holati"
    )
    
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    applications_count = models.PositiveIntegerField(default=0, verbose_name="Откликлар soni")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ish e'loni"
        verbose_name_plural = "Ish e'lonlari"
        ordering = ['-created_at']

    def __str__(self):
        pos = self.position.name_uz if self.position else (self.custom_position_name or 'Ish')
        return f"JobPost #{self.id}: {pos} ({self.district or 'Hudud'}) - {self.get_status_display()}"


class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', "Kutilmoqda"
        ACCEPTED = 'accepted', "Qabul qilindi"
        REJECTED = 'rejected', "Rad etildi"

    job_post = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name="Ish e'loni"
    )
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_applications',
        verbose_name="Ishchi / Usta"
    )
    proposal_message = models.TextField(blank=True, null=True, verbose_name="Usta taklif xabari")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Holat"
    )
    is_deleted_by_worker = models.BooleanField(default=False, verbose_name="Ishchi tomonidan o'chirilgan")
    is_deleted_by_employer = models.BooleanField(default=False, verbose_name="Ish beruvchi tomonidan o'chirilgan")
    is_invited = models.BooleanField(default=False, verbose_name="Ish taklifi sifatida yuborilgan (5km yoki moslik)")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ishga murojaat (Отклик)"
        verbose_name_plural = "Ishga murojaatlar (Откликлар)"
        unique_together = ('job_post', 'worker')
        ordering = ['-applied_at']

    def __str__(self):
        return f"Application #{self.id} on Job #{self.job_post_id} by {self.worker}"

