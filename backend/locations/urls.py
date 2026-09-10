from django.urls import path
from .views import UpdateLocationView, LiveWorkerLocationsView

urlpatterns = [
    path('update/', UpdateLocationView.as_view(), name='update-location'),
    path('live-workers/', LiveWorkerLocationsView.as_view(), name='live-workers'),
]
