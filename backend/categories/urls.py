from django.urls import path
from .views import CategoryListCreateView, CategoryDetailView, PositionListCreateView, PositionDetailView

urlpatterns = [
    path('', CategoryListCreateView.as_view(), name='category-list-create'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('positions/', PositionListCreateView.as_view(), name='position-list-create'),
    path('positions/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
]

