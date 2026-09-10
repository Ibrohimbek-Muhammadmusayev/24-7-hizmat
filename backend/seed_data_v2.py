import os
import sys
import django

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from locations.models import Region
from categories.models import Category, Position
from accounts.models import User

def populate():
    print("=== SEED DATA V2 BOSHLANDI ===")

    # 1. Viloyatlar va Shaharlar (4 tilda)
    regions_data = [
        {"uz": "Toshkent shahri", "oz": "Тошкент шаҳри", "ru": "город Ташкент", "en": "Tashkent City", "order": 1},
        {"uz": "Toshkent viloyati", "oz": "Тошкент вилояти", "ru": "Ташкентская область", "en": "Tashkent Region", "order": 2},
        {"uz": "Andijon viloyati", "oz": "Андижон вилояти", "ru": "Андижанская область", "en": "Andijan Region", "order": 3},
        {"uz": "Buxoro viloyati", "oz": "Бухоро вилояти", "ru": "Бухарская область", "en": "Bukhara Region", "order": 4},
        {"uz": "Farg'ona viloyati", "oz": "Фарғона вилояти", "ru": "Ферганская область", "en": "Fergana Region", "order": 5},
        {"uz": "Jizzax viloyati", "oz": "Жиззах вилояти", "ru": "Джизакская область", "en": "Jizzakh Region", "order": 6},
        {"uz": "Xorazm viloyati", "oz": "Хоразм вилояти", "ru": "Хорезмская область", "en": "Khorezm Region", "order": 7},
        {"uz": "Namangan viloyati", "oz": "Наманган вилояти", "ru": "Наманганская область", "en": "Namangan Region", "order": 8},
        {"uz": "Navoiy viloyati", "oz": "Навоий вилояти", "ru": "Навоийская область", "en": "Navoi Region", "order": 9},
        {"uz": "Qashqadaryo viloyati", "oz": "Қашқадарё вилояти", "ru": "Кашкадарьинская область", "en": "Kashkadarya Region", "order": 10},
        {"uz": "Qoraqalpog'iston Respublikasi", "oz": "Қорақалпоғистон Республикаси", "ru": "Республика Каракалпакстан", "en": "Republic of Karakalpakstan", "order": 11},
        {"uz": "Samarqand viloyati", "oz": "Самарқанд вилояти", "ru": "Самаркандская область", "en": "Samarkand Region", "order": 12},
        {"uz": "Sirdaryo viloyati", "oz": "Сирдарё вилояти", "ru": "Сырдарьинская область", "en": "Sirdaryo Region", "order": 13},
        {"uz": "Surxondaryo viloyati", "oz": "Сурхондарё вилояти", "ru": "Сурхандарьинская область", "en": "Surkhandarya Region", "order": 14},
    ]

    for reg in regions_data:
        region, created = Region.objects.update_or_create(
            name_uz=reg["uz"],
            defaults={
                "name_oz": reg["oz"],
                "name_ru": reg["ru"],
                "name_en": reg["en"],
                "order": reg["order"],
                "is_active": True
            }
        )
        if created:
            print(f" [Viloyat qo'shildi]: {reg['uz']}")

    # 2. Sohalar va Lavozimlar (4 tilda)
    categories_data = [
        {
            "icon": "💻",
            "order": 1,
            "uz": "Axborot Texnologiyalari (IT)",
            "oz": "Ахборот Технологиялари (IT)",
            "ru": "Информационные Технологии (IT)",
            "en": "Information Technology (IT)",
            "positions": [
                {"uz": "Frontend Dasturchi", "oz": "Frontend Дастурчи", "ru": "Frontend Разработчик", "en": "Frontend Developer"},
                {"uz": "Backend Dasturchi", "oz": "Backend Дастурчи", "ru": "Backend Разработчик", "en": "Backend Developer"},
                {"uz": "Mobil Dasturchi (Flutter/iOS/Android)", "oz": "Мобил Дастурчи", "ru": "Мобильный разработчик", "en": "Mobile Developer"},
                {"uz": "UI/UX Dizayner", "oz": "UI/UX Дизайнер", "ru": "UI/UX Дизайнер", "en": "UI/UX Designer"},
                {"uz": "IT Operator / Texnik qo'llab-quvvatlash", "oz": "IT Оператор / Техник ёрдам", "ru": "IT Оператор / Техподдержка", "en": "IT Support Operator"},
                {"uz": "Tizim Administratori (SysAdmin)", "oz": "Тизим Администратори", "ru": "Системный администратор", "en": "System Administrator"},
                {"uz": "Loyiha Menejeri (Project Manager)", "oz": "Лойиҳа Менежери", "ru": "Менеджер проектов", "en": "Project Manager"},
            ]
        },
        {
            "icon": "🏗️",
            "order": 2,
            "uz": "Qurilish va Ta'mirlash",
            "oz": "Қурилиш ва Таъмирлаш",
            "ru": "Строительство и Ремонт",
            "en": "Construction and Renovation",
            "positions": [
                {"uz": "Qurilish boshqaruvchisi / Prorab", "oz": "Қурилиш бошқарувчиси / Прораб", "ru": "Прораб / Начальник стройки", "en": "Site Supervisor / Foreman"},
                {"uz": "Santexnik (Usta)", "oz": "Сантехник (Уста)", "ru": "Сантехник (Мастер)", "en": "Plumber"},
                {"uz": "Elektrik (Usta)", "oz": "Электрик (Уста)", "ru": "Электрик (Мастер)", "en": "Electrician"},
                {"uz": "Kafel teruvchi (Usta)", "oz": "Кафель терувчи", "ru": "Плиточник", "en": "Tiler"},
                {"uz": "Gipsokarton va Malyar", "oz": "Гипсокартон ва Маляр", "ru": "Гипсокартонщик и Маляр", "en": "Drywall & Painter"},
                {"uz": "Payvandchi (Svarchik)", "oz": "Пайвандчи (Сварчик)", "ru": "Сварщик", "en": "Welder"},
                {"uz": "G'isht teruvchi va Suvoqchi", "oz": "Ғишт терувчи ва Сувоқчи", "ru": "Каменщик и Штукатур", "en": "Mason & Plasterer"},
            ]
        },
        {
            "icon": "🛍️",
            "order": 3,
            "uz": "Savdo va Xizmat ko'rsatish",
            "oz": "Савдо ва Хизмат кўрсатиш",
            "ru": "Продажи и Торговля",
            "en": "Sales and Retail",
            "positions": [
                {"uz": "Kassir / G'aznachi", "oz": "Кассир / Ғазначи", "ru": "Кассир", "en": "Cashier"},
                {"uz": "Sotuvchi-maslahatchi", "oz": "Сотувчи-маслаҳатчи", "ru": "Продавец-консультант", "en": "Sales Consultant"},
                {"uz": "Do'kon Boshqaruvchisi / Administrator", "oz": "Дўкон Бошқарувчиси", "ru": "Управляющий магазином", "en": "Store Manager"},
                {"uz": "Mijozlar bilan ishlash operatori", "oz": "Мижозлар билан ишлаш оператори", "ru": "Оператор по работе с клиентами", "en": "Customer Service Operator"},
                {"uz": "Savdo agenti (Savdo vakili)", "oz": "Савдо агенти", "ru": "Торговый представитель", "en": "Sales Representative"},
            ]
        },
        {
            "icon": "🍽️",
            "order": 4,
            "uz": "Restoran va Umumiy Ovqatlanish",
            "oz": "Ресторан ва Умумий Овқатланиш",
            "ru": "Рестораны и Общепит",
            "en": "Restaurants and Catering",
            "positions": [
                {"uz": "Bosh oshpaz (Shef-povar)", "oz": "Бош ошпаз (Шеф-повар)", "ru": "Шеф-повар", "en": "Head Chef"},
                {"uz": "Oshpaz yordamchisi", "oz": "Ошпаз ёрдамчиси", "ru": "Помощник повара", "en": "Assistant Cook"},
                {"uz": "Ofitsiant (Xizmatchi)", "oz": "Официант (Хизматчи)", "ru": "Официант", "en": "Waiter / Waitress"},
                {"uz": "Barista / Barmen", "oz": "Бариста / Бармен", "ru": "Бариста / Бармен", "en": "Barista / Bartender"},
                {"uz": "Restoran Menejeri / Administrator", "oz": "Ресторан Менежери", "ru": "Администратор ресторана", "en": "Restaurant Manager"},
                {"uz": "Idish yuvuvchi va Tozalovchi", "oz": "Идиш ювувчи ва Тозаловчи", "ru": "Посудомойщик", "en": "Dishwasher"},
            ]
        },
        {
            "icon": "🚗",
            "order": 5,
            "uz": "Transport va Haydovchilik",
            "oz": "Транспорт ва Ҳайдовчилик",
            "ru": "Транспорт и Вождение",
            "en": "Transport and Driving",
            "positions": [
                {"uz": "Yuk mashinasi haydovchisi", "oz": "Юк машинаси ҳайдовчиси", "ru": "Водитель грузовика", "en": "Truck Driver"},
                {"uz": "Yetkazib beruvchi (Kuryer)", "oz": "Етказиб берувчи (Курьер)", "ru": "Курьер / Доставщик", "en": "Courier / Delivery Driver"},
                {"uz": "Shaxsiy / Taksi haydovchisi", "oz": "Шахсий / Такси ҳайдовчиси", "ru": "Персональный / Такси водитель", "en": "Personal / Taxi Driver"},
                {"uz": "Avtomexanik (Usta)", "oz": "Автомеханик (Уста)", "ru": "Автомеханик (Мастер)", "en": "Car Mechanic"},
                {"uz": "Avtoelektrik", "oz": "Автоэлектрик", "ru": "Автоэлектрик", "en": "Auto Electrician"},
                {"uz": "Dispetcher / Logist", "oz": "Диспетчер / Логист", "ru": "Диспетчер / Логист", "en": "Dispatcher / Logistician"},
            ]
        },
        {
            "icon": "🏭",
            "order": 6,
            "uz": "Ishlab Chiqarish va Sanoat",
            "oz": "Ишлаб Чиқариш ва Саноат",
            "ru": "Производство и Промышленность",
            "en": "Manufacturing and Production",
            "positions": [
                {"uz": "Sex boshlig'i / Boshqaruvchi", "oz": "Цех бошлиғи / Бошқарувчи", "ru": "Начальник цеха / Управляющий", "en": "Production Manager"},
                {"uz": "Stanok operatori / Usta", "oz": "Станок оператори / Уста", "ru": "Оператор станков", "en": "Machine Operator"},
                {"uz": "Tikuvchi / Bichuvchi", "oz": "Тикувчи / Бичувчи", "ru": "Швея / Закройщик", "en": "Tailor / Seamstress"},
                {"uz": "Qadoqlovchi va Joylovchi", "oz": "Қадоқловчи ва Жойловчи", "ru": "Упаковщик / Комплектовщик", "en": "Packer"},
                {"uz": "Omborchi (Zavsklad)", "oz": "Омборчи (Завсклад)", "ru": "Кладовщик", "en": "Warehouse Keeper"},
            ]
        },
        {
            "icon": "📚",
            "order": 7,
            "uz": "Ta'lim va Fan",
            "oz": "Таълим ва Фан",
            "ru": "Образование и Наука",
            "en": "Education and Training",
            "positions": [
                {"uz": "Ingliz tili o'qituvchisi", "oz": "Инглиз тили ўқитувчиси", "ru": "Преподаватель английского", "en": "English Teacher"},
                {"uz": "Matematika / Aniq fanlar o'qituvchisi", "oz": "Математика ўқитувчиси", "ru": "Учитель математики", "en": "Math Teacher"},
                {"uz": "O'quv markazi administratori", "oz": "Ўқув маркази администратори", "ru": "Администратор учебного центра", "en": "Education Center Admin"},
                {"uz": "Maktabgacha ta'lim tarbiyachisi", "oz": "Тарбиячи", "ru": "Воспитатель", "en": "Kindergarten Teacher"},
                {"uz": "Repetitor / Shaxsiy repetitor", "oz": "Репетитор", "ru": "Репетитор", "en": "Private Tutor"},
            ]
        },
        {
            "icon": "🏥",
            "order": 8,
            "uz": "Tibbiyot va Farmatsevtika",
            "oz": "Тиббиёт ва Фармацевтика",
            "ru": "Медицина и Фармацевтика",
            "en": "Medicine and Healthcare",
            "positions": [
                {"uz": "Shifokor (Vratch)", "oz": "Шифокор (Врач)", "ru": "Врач", "en": "Doctor"},
                {"uz": "Hamshira (Medsektra)", "oz": "Ҳамшира (Медсестра)", "ru": "Медсестра / Медбрат", "en": "Nurse"},
                {"uz": "Farmatsevt / Provizor (Dorixona)", "oz": "Фармацевт / Провизор", "ru": "Фармацевт / Провизор", "en": "Pharmacist"},
                {"uz": "Laborant", "oz": "Лаборант", "ru": "Лаборант", "en": "Laboratory Assistant"},
                {"uz": "Massajchi / Terapevt", "oz": "Массажчи", "ru": "Массажист / Терапевт", "en": "Massage Therapist"},
            ]
        },
        {
            "icon": "💼",
            "order": 9,
            "uz": "Moliya va Buxgalteriya",
            "oz": "Молия ва Бухгалтерия",
            "ru": "Финансы и Бухгалтерия",
            "en": "Finance and Accounting",
            "positions": [
                {"uz": "Bosh buxgalter", "oz": "Бош бухгалтер", "ru": "Главный бухгалтер", "en": "Chief Accountant"},
                {"uz": "Buxgalter yordamchisi (1C)", "oz": "Бухгалтер ёрдамчиси (1C)", "ru": "Помощник бухгалтера (1C)", "en": "Accountant Assistant"},
                {"uz": "Moliyaviy tahlilchi / Iqtisodchi", "oz": "Молиявий таҳлилчи", "ru": "Финансовый аналитик", "en": "Financial Analyst"},
                {"uz": "Auditor", "oz": "Аудитор", "ru": "Аудитор", "en": "Auditor"},
            ]
        },
        {
            "icon": "🧹",
            "order": 10,
            "uz": "Tozalash va Klining xizmati",
            "oz": "Тозалаш ва Клининг хизмати",
            "ru": "Клининг и Уборка",
            "en": "Cleaning Services",
            "positions": [
                {"uz": "Klining ustasi (Professional tozalash)", "oz": "Клининг устаси", "ru": "Мастер клининга", "en": "Cleaning Specialist"},
                {"uz": "Farrosh / Tozalik xodimi", "oz": "Фаррош", "ru": "Уборщик / Уборщица", "en": "Cleaner / Janitor"},
                {"uz": "Mebel va Gilam yuvish ustasi", "oz": "Мебель ва Гилам ювиш устаси", "ru": "Мастер химчистки", "en": "Carpet & Furniture Cleaner"},
            ]
        },
        {
            "icon": "🛡️",
            "order": 11,
            "uz": "Xavfsizlik va Qo'riqlash",
            "oz": "Хавфсизлик ва Қўриқлаш",
            "ru": "Безопасность и Охрана",
            "en": "Security and Guarding",
            "positions": [
                {"uz": "Qo'riqchi (Oxrannik)", "oz": "Қўриқчи (Охранник)", "ru": "Охранник", "en": "Security Guard"},
                {"uz": "Xavfsizlik xizmati boshlig'i", "oz": "Хавфсизлик бошлиғи", "ru": "Начальник службы безопасности", "en": "Chief of Security"},
                {"uz": "Kuzatuv kameralari operatori", "oz": "Кузатув камералари оператори", "ru": "Оператор видеонаблюдения", "en": "CCTV Operator"},
            ]
        },
        {
            "icon": "💄",
            "order": 12,
            "uz": "Go'zallik va Salomatlik",
            "oz": "Гўзаллик ва Саломатлик",
            "ru": "Красота и Здоровье",
            "en": "Beauty and Wellness",
            "positions": [
                {"uz": "Sartarosh / Stilist (Erkaklar/Ayollar)", "oz": "Сартарош / Стилист", "ru": "Парикмахер / Стилист", "en": "Hair Stylist / Barber"},
                {"uz": "Vizajist / Kosmetolog", "oz": "Визажист / Косметолог", "ru": "Визажист / Косметолог", "en": "Visagiste / Cosmetologist"},
                {"uz": "Manikyur / Pedikyur ustasi", "oz": "Маникюр / Педикюр устаси", "ru": "Мастер маникюра", "en": "Nail Master"},
            ]
        },
    ]

    for cat_data in categories_data:
        cat, _ = Category.objects.update_or_create(
            name_uz=cat_data["uz"],
            defaults={
                "name_oz": cat_data["oz"],
                "name_ru": cat_data["ru"],
                "name_en": cat_data["en"],
                "icon": cat_data["icon"],
                "order": cat_data["order"],
                "is_active": True
            }
        )
        print(f" [Soha]: {cat.icon} {cat.name_uz}")
        
        for p_idx, pos_data in enumerate(cat_data["positions"], start=1):
            pos, _ = Position.objects.update_or_create(
                category=cat,
                name_uz=pos_data["uz"],
                defaults={
                    "name_oz": pos_data["oz"],
                    "name_ru": pos_data["ru"],
                    "name_en": pos_data["en"],
                    "order": p_idx,
                    "is_active": True
                }
            )

    # Superuser tekshirish / yaratish
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@fullxizmat.uz', 'admin123')
        admin_user.role = User.Role.ADMIN
        admin_user.first_name = 'Super Admin'
        admin_user.phone_number = '+998901234567'
        admin_user.save()
        print(" [Superuser yaratildi]: login: admin, parol: admin123")

    print("=== SEED DATA V2 MUVAFFAQIYATLI YAKUNLANDI ===")

if __name__ == '__main__':
    populate()
