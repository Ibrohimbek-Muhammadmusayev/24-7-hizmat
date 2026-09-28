from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import render

def dynamic_domain_view(request, *args, **kwargs):
    """
    Subdomain & Route Router:
    1. Agar host 'admin.*' bo'lsa yoki URL yo'li '/dashboard' bo'lsa -> React Admin Dashboard (index.html)
    2. Agar URL yo'li '/app', '/webapp' yoki query param 'tg_id', 'view=webapp' bo'lsa -> React Web App (index.html)
    3. Aks holda asosiy domen (domain.uz / 127.0.0.1) -> Bosh sahifa (landing.html)
    """
    host = request.get_host().lower()
    path = request.path
    query = request.META.get('QUERY_STRING', '')

    is_webapp = (
        path.startswith('/app') or 
        path.startswith('/webapp') or 
        'view=webapp' in query or 
        'tg_id=' in query
    )
    is_admin = host.startswith('admin.') or path.startswith('/dashboard')

    if is_admin or is_webapp:
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
