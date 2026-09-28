from django.urls import path
from .views import UpdateLocationView, LiveWorkerLocationsView, RegionListView

urlpatterns = [
    path('update/', UpdateLocationView.as_view(), name='update-location'),
    path('live-workers/', LiveWorkerLocationsView.as_view(), name='live-workers'),
    path('regions/', RegionListView.as_view(), name='region-list'),
]
