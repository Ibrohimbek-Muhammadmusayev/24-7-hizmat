from django.urls import re_path
from locations import consumers

websocket_urlpatterns = [
    re_path(r'ws/live-map/$', consumers.LiveMapConsumer.as_asgi()),
    re_path(r'ws/worker-alerts/(?P<worker_id>\d+)/$', consumers.WorkerAlertConsumer.as_asgi()),
]
