from django.db import models
from django.conf import settings

class Region(models.Model):
    name_uz = models.CharField(max_length=150, default='', verbose_name="Viloyat/Shahar (O'zbek Lotin)")
    name_oz = models.CharField(max_length=150, verbose_name="Вилоят/Шаҳар (Ўзбек Кирилл)", blank=True, null=True)
    name_ru = models.CharField(max_length=150, verbose_name="Область/Город (Русский)", blank=True, null=True)
    name_en = models.CharField(max_length=150, verbose_name="Region/City (English)", blank=True, null=True)
    
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Viloyat / Hudud"
        verbose_name_plural = "Viloyatlar va Hududlar"
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
        return self.name_uz


class WorkerLocation(models.Model):
    worker = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='current_location'
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    heading = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.worker.first_name or self.worker.username} location: ({self.latitude}, {self.longitude})"


import urllib.request
import json
import logging

logger = logging.getLogger(__name__)

REGION_KEYWORDS = {
    'toshkent shahri': ['toshkent shahri', 'tashkent city', 'город ташкент', 'tashkent'],
    'toshkent viloyati': ['toshkent viloyati', 'tashkent region', 'ташкентская область'],
    'andijon viloyati': ['andijon', 'andijan', 'андижан'],
    'buxoro viloyati': ['buxoro', 'bukhara', 'бухара'],
    'farg\'ona viloyati': ['farg\'ona', 'fergana', 'фергана', 'fargona'],
    'jizzax viloyati': ['jizzax', 'jizzakh', 'джизак'],
    'xorazm viloyati': ['xorazm', 'khorezm', 'хорезм', 'urganch', 'urgench'],
    'namangan viloyati': ['namangan', 'наманган'],
    'navoiy viloyati': ['navoiy', 'navoi', 'навои'],
    'qashqadaryo viloyati': ['qashqadaryo', 'kashkadarya', 'кашкадарья', 'qarshi', 'karshi'],
    'qoraqalpog\'iston respublikasi': ['qoraqalpog\'iston', 'karakalpakstan', 'каракалпакстан', 'nukus', 'nukis'],
    'samarqand viloyati': ['samarqand', 'samarkand', 'самарканд'],
    'sirdaryo viloyati': ['sirdaryo', 'sirdaryo viloyati', 'syrdarya', 'сырдарья', 'guliston', 'gulistan'],
    'surxondaryo viloyati': ['surxondaryo', 'surkhandarya', 'сурхандарья', 'termiz', 'termez'],
}

def reverse_geocode(lat: float, lon: float):
    """
    OpenStreetMap Nominatim orqali koordinatadan Viloyat, Tuman/Shahar va Mahallani aniqlash
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=uz"
        headers = {'User-Agent': 'FullXizmatBot/2.0 (contact@fullxizmat.uz)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            address = data.get('address', {})
            
            raw_state = address.get('state', '') or address.get('region', '') or address.get('city', '')
            district = address.get('county', '') or address.get('city_district', '') or address.get('suburb', '') or address.get('district', '') or address.get('town', '') or address.get('village', '') or address.get('city', '')
            road = address.get('road', '') or address.get('neighbourhood', '') or address.get('suburb', '')
            
            matched_region_name = None
            search_str = f"{raw_state} {district} {address.get('city', '')}".lower()
            
            for reg_canonical, keywords in REGION_KEYWORDS.items():
                for kw in keywords:
                    if kw in search_str:
                        matched_region_name = reg_canonical
                        break
                if matched_region_name:
                    break
            
            return {
                'raw_state': raw_state,
                'region_name': matched_region_name or raw_state,
                'district': district,
                'road': road,
                'display_name': data.get('display_name', '')
            }
    except Exception as e:
        logger.error(f"Reverse geocode error: {e}")
        return {
            'raw_state': '',
            'region_name': '',
            'district': '',
            'road': '',
            'display_name': ''
        }

