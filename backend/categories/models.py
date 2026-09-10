from django.db import models

class Category(models.Model):
    name_uz = models.CharField(max_length=150, default='', verbose_name="Nomi (O'zbek Lotin)")
    name_oz = models.CharField(max_length=150, verbose_name="Номи (Ўзбек Кирилл)", blank=True, null=True)
    name_ru = models.CharField(max_length=150, verbose_name="Название (Русский)", blank=True, null=True)
    name_en = models.CharField(max_length=150, verbose_name="Name (English)", blank=True, null=True)
    
    icon = models.CharField(max_length=30, default='🛠️', verbose_name="Ikonka (Emoji)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Soha / Yo'nalish"
        verbose_name_plural = "Sohalar va Yo'nalishlar"
        ordering = ['order', 'id']

    @property
    def name(self):
        return self.name_uz

    def get_name(self, lang='uz'):
        if lang == 'oz' and self.name_oz:
            return self.name_oz
        elif lang == 'ru' and self.name_ru:
            return self.name_ru
        elif lang == 'en' and self.name_en:
            return self.name_en
        return self.name_uz or str(self.id)

    def __str__(self):
        return f"{self.icon} {self.name_uz}"


class Position(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name="Tegishli Soha"
    )
    name_uz = models.CharField(max_length=150, default='', verbose_name="Lavozim nomi (O'zbek Lotin)")
    name_oz = models.CharField(max_length=150, verbose_name="Лавозим номи (Ўзбек Кирилл)", blank=True, null=True)
    name_ru = models.CharField(max_length=150, verbose_name="Название должности (Русский)", blank=True, null=True)
    name_en = models.CharField(max_length=150, verbose_name="Position Name (English)", blank=True, null=True)
    
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lavozim / Mutaxassislik"
        verbose_name_plural = "Lavozimlar va Mutaxassisliklar"
        ordering = ['order', 'id']

    @property
    def name(self):
        return self.name_uz

    def get_name(self, lang='uz'):
        if lang == 'oz' and self.name_oz:
            return self.name_oz
        elif lang == 'ru' and self.name_ru:
            return self.name_ru
        elif lang == 'en' and self.name_en:
            return self.name_en
        return self.name_uz or str(self.id)

    def __str__(self):
        return f"{self.name_uz} ({self.category.name_uz})"
