from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import render

def dynamic_domain_view(request, *args, **kwargs):
    """
    Subdomain Router:
    1. Agar host 'admin.*' bo'lsa -> React Admin Dashboard (index.html)
    2. Agar URL yo'li '/dashboard/' bo'lsa -> React Admin Dashboard (index.html)
    3. Aks holda asosiy domen (domain.uz / 127.0.0.1) -> Bosh sahifa (landing.html)
    """
    host = request.get_host().lower()
    path = request.path

    # Subdomain (admin.domain.uz) yoki /dashboard/ yo'li bo'lsa
    if host.startswith('admin.') or path.startswith('/dashboard'):
        return render(request, 'index.html')
    
    # Asosiy domen (bosh sahifa)
    return render(request, 'landing.html')

urlpatterns = [
    # Djangoning ichki ma'lumotlar bazasi boshqaruvi
    path('django-admin/', admin.site.urls),

    # REST API endpoints
    path('api/categories/', include('categories.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/locations/', include('locations.urls')),
    path('api/bot/', include('bot_control.urls')),

    # React Admin Dashboard (Toza URL)
    re_path(r'^dashboard(/.*)?$', dynamic_domain_view),

    # Asosiy domen / Boshqa yo'nalishlar
    re_path(r'^(?!api|django-admin|static).*$', dynamic_domain_view),
]
