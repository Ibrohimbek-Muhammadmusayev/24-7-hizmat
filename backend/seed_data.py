import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from categories.models import Category
from accounts.models import User
from orders.models import Order
from locations.models import WorkerLocation

def seed():
    print("Seeding initial Categories & Accounts...")

    # Default Categories
    categories_data = [
        {'name': 'Santexnik', 'icon': '🔧', 'description': "Jo'mrak, truba va santexnika xizmatlari"},
        {'name': 'Elektrik', 'icon': '⚡', 'description': "Elektr montaj va maishiy jihozlar nosozliklari"},
        {'name': 'Maishiy Usta', 'icon': '🔨', 'description': "Uy-ro'zg'or buyumlarini tuzatish va o'rnatish"},
        {'name': 'Tozalash', 'icon': '🧹', 'description': "Xonadon va ofis tozalash (Cleaning)"},
        {'name': "Mebel Yig'ish", 'icon': '🛋️', 'description': "Mebel yig'ish va ta'mirlash xizmati"},
        {'name': 'Avto-Xizmat', 'icon': '🚗', 'description': "Avtomobil ta'mirlash va evakuator"},
    ]

    categories = {}
    for cdata in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cdata['name'],
            defaults={'icon': cdata['icon'], 'description': cdata['description']}
        )
        categories[cat.name] = cat
        if created:
            print(f"Created Category: {cat.name}")

    # Admin User
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'Super',
            'last_name': 'Admin',
            'phone_number': '+998900000000',
            'role': User.Role.ADMIN,
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created Admin user: admin / admin123")

    # Call Center Operator User
    operator_user, created = User.objects.get_or_create(
        username='operator',
        defaults={
            'first_name': 'CallCenter',
            'last_name': 'Operator',
            'phone_number': '+998901112233',
            'role': User.Role.CALL_CENTER,
            'is_staff': False
        }
    )
    if created:
        operator_user.set_password('operator123')
        operator_user.save()
        print("Created Operator user: operator / operator123")

    # Worker 1 (Santexnik)
    worker1, created = User.objects.get_or_create(
        username='worker1',
        defaults={
            'first_name': 'Dilshod',
            'last_name': 'Karimov',
            'phone_number': '+998909876543',
            'role': User.Role.WORKER,
            'category': categories.get('Santexnik'),
            'specialty': 'Santexnik',
            'is_online': True,
            'rating': 4.9
        }
    )
    if created:
        worker1.set_password('worker123')
        worker1.save()
        print("Created Worker 1: worker1 / worker123 (Santexnik)")

        WorkerLocation.objects.get_or_create(
            worker=worker1,
            defaults={'latitude': 41.311081, 'longitude': 69.240562, 'heading': 90.0}
        )

    # Worker 2 (Elektrik)
    worker2, created = User.objects.get_or_create(
        username='worker2',
        defaults={
            'first_name': 'Jasur',
            'last_name': 'Axmedov',
            'phone_number': '+998905554433',
            'role': User.Role.WORKER,
            'category': categories.get('Elektrik'),
            'specialty': 'Elektrik',
            'is_online': True,
            'rating': 4.8
        }
    )
    if created:
        worker2.set_password('worker123')
        worker2.save()
        print("Created Worker 2: worker2 / worker123 (Elektrik)")

        WorkerLocation.objects.get_or_create(
            worker=worker2,
            defaults={'latitude': 41.325000, 'longitude': 69.260000, 'heading': 45.0}
        )

    # Sample Pending Order
    order, created = Order.objects.get_or_create(
        customer_name='Shaxzod Rahimov',
        defaults={
            'source': Order.Source.CALL_CENTER,
            'category': categories.get('Santexnik'),
            'title': "Jo'mrak tuzatish xizmati",
            'customer_phone': '+998977778899',
            'address': 'Toshkent sh., Yunusobod 4-dahshat, 15-uy',
            'latitude': 41.330000,
            'longitude': 69.280000,
            'service_type': 'Santexnik',
            'description': "Jo'mrakdan suv tomayapti, almashtirish kerak.",
            'price': 60000.00,
            'status': Order.Status.PENDING
        }
    )
    if created:
        print(f"Created sample pending order #{order.id}")

    print("Seed data creation complete!")

if __name__ == '__main__':
    seed()
