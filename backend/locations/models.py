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
import ssl

logger = logging.getLogger(__name__)

# SSL verification context (certifi yoki unverified fallback)
try:
    import certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
except Exception:
    ssl_context = ssl._create_unverified_context()

# ISO3166-2-lvl4 mapping and comprehensive keywords
ISO_REGION_MAP = {
    'UZ-TK': 1,   # Toshkent shahri
    'UZ-TO': 2,   # Toshkent viloyati
    'UZ-AN': 3,   # Andijon viloyati
    'UZ-BU': 4,   # Buxoro viloyati
    'UZ-FA': 5,   # Farg'ona viloyati
    'UZ-JI': 6,   # Jizzax viloyati
    'UZ-XO': 7,   # Xorazm viloyati
    'UZ-NG': 8,   # Namangan viloyati
    'UZ-NW': 9,   # Navoiy viloyati
    'UZ-QA': 10,  # Qashqadaryo viloyati
    'UZ-QR': 11,  # Qoraqalpog'iston Respublikasi
    'UZ-SA': 12,  # Samarqand viloyati
    'UZ-SI': 13,  # Sirdaryo viloyati
    'UZ-SU': 14,  # Surxondaryo viloyati
}

REGION_KEYWORDS = {
    1: ['toshkent shahri', 'tashkent city', 'город ташкент', 'toshkent shahar', 'tashkent'],
    2: ['toshkent viloyati', 'tashkent region', 'ташкентская область', 'chirchiq', 'angren', 'olmaliq', 'bekobod', 'yangiyo‘l', 'yangiyul', 'parkent'],
    3: ['andijon', 'andijan', 'андижан', 'asaka', 'xonobod', 'shahrixon'],
    4: ['buxoro', 'bukhara', 'бухара', 'kogon', 'g‘ijduvon', 'gijduvon'],
    5: ['farg‘ona', 'farg\'ona', 'fergana', 'фергана', 'fargona', 'qo‘qon', 'qoqon', 'quva', 'marg‘ilon', 'margilon', 'rishton'],
    6: ['jizzax', 'jizzakh', 'джизак', 'zomin', 'g‘allaorol', 'do‘stlik'],
    7: ['xorazm', 'khorezm', 'хорезм', 'urganch', 'urgench', 'xiva', 'khiva'],
    8: ['namangan', 'наманган', 'chust', 'pop', 'kosonsoy', 'uchqo‘rg‘on'],
    9: ['navoiy', 'navoi', 'навои', 'zarafshon', 'karmana', 'uchquduq'],
    10: ['qashqadaryo', 'kashkadarya', 'кашкадарья', 'qarshi', 'karshi', 'shahrisabz', 'shaxrisabz', 'koson', 'kitob', 'muborak'],
    11: ['qoraqalpog‘iston', 'qoraqalpog\'iston', 'karakalpakstan', 'каракалпакстан', 'nukus', 'nukis', 'qo‘ng‘irot', 'xo‘jayli'],
    12: ['samarqand', 'samarkand', 'самарканд', 'kattaqo‘rg‘on', 'urgut', 'pastdarg‘om'],
    13: ['sirdaryo', 'syrdarya', 'сырдарья', 'guliston', 'gulistan', 'yangiyer', 'shirin', 'boyovut'],
    14: ['surxondaryo', 'surkhandarya', 'сурхандарья', 'termiz', 'termez', 'denov', 'sherobod', 'boysun'],
}

def reverse_geocode(lat: float, lon: float):
    """
    OpenStreetMap Nominatim orqali koordinatadan Viloyat, Tuman/Shahar va Mahallani aniqlash
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=uz"
        headers = {'User-Agent': 'Ishtop24Platform/2.0 (admin@ishtop24.uz)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6, context=ssl_context) as response:
            data = json.loads(response.read().decode('utf-8'))
            address = data.get('address', {})
            
            iso_code = address.get('ISO3166-2-lvl4', '')
            raw_state = address.get('state', '') or address.get('region', '')
            city = address.get('city', '') or address.get('town', '') or address.get('village', '')
            county = address.get('county', '')
            district_key = address.get('city_district', '') or address.get('district', '') or address.get('suburb', '')
            road = address.get('road', '') or address.get('neighbourhood', '')

            # 1. District / Tuman aniqlash
            # County, city_district, suburb yoki city lardan birini eng aniq tuman sifatida olamiz
            district = ""
            for candidate in [county, district_key, city, address.get('suburb'), address.get('neighbourhood')]:
                if candidate and candidate.strip():
                    district = candidate.strip()
                    break

            # 2. Region ID aniqlash
            matched_region_id = None
            if iso_code and iso_code in ISO_REGION_MAP:
                matched_region_id = ISO_REGION_MAP[iso_code]
            
            # Agar ISO code bo'lmasa yoki aniqlanmasa, matnli qidiruv
            if not matched_region_id:
                full_text = f"{raw_state} {city} {county} {district_key} {data.get('display_name', '')}".lower()
                # Maxsus: Toshkent viloyati vs Toshkent shahri
                if 'toshkent viloyati' in full_text or 'ташкентская область' in full_text:
                    matched_region_id = 2
                elif 'toshkent' in full_text or 'tashkent' in full_text:
                    matched_region_id = 1
                else:
                    for reg_id, keywords in REGION_KEYWORDS.items():
                        if any(kw in full_text for kw in keywords):
                            matched_region_id = reg_id
                            break

            # Region obyektini olish
            region_obj = None
            if matched_region_id:
                region_obj = Region.objects.filter(id=matched_region_id).first()
            if not region_obj and raw_state:
                region_obj = Region.objects.filter(name_uz__icontains=raw_state[:6]).first()

            region_name = region_obj.name_uz if region_obj else (raw_state or "O'zbekiston")

            return {
                'raw_state': raw_state,
                'region_id': region_obj.id if region_obj else None,
                'region_name': region_name,
                'district': district or road,
                'road': road,
                'display_name': data.get('display_name', '')
            }
    except Exception as e:
        logger.error(f"Reverse geocode error: {e}")
        # Koordinata bo'yicha taxminiy hudud (Toshkent koordinatalari uchun default)
        region_obj = None
        if 41.15 <= lat <= 41.45 and 69.10 <= lon <= 69.45:
            region_obj = Region.objects.filter(id=1).first() # Toshkent shahri
        return {
            'raw_state': '',
            'region_id': region_obj.id if region_obj else None,
            'region_name': region_obj.name_uz if region_obj else "O'zbekiston",
            'district': '',
            'road': '',
            'display_name': ''
        }
