from django.urls import path
from .views import (
    OrderListCreateView, OrderDetailView, DispatchOrderView, UpdateOrderStatusView, 
    WorkerJobHistoryView, OrderStatsView, JobPostListCreateView, JobPostDetailView, 
    OfferJobToWorkerView
)

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('stats/', OrderStatsView.as_view(), name='order-stats'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/dispatch/', DispatchOrderView.as_view(), name='order-dispatch'),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view(), name='order-status'),
    path('worker-history/', WorkerJobHistoryView.as_view(), name='worker-history'),
    
    # Job Posts (Ish e'lonlari) CRUD & Offer
    path('job-posts/', JobPostListCreateView.as_view(), name='job-post-list-create'),
    path('job-posts/<int:pk>/', JobPostDetailView.as_view(), name='job-post-detail'),
    path('job-posts/<int:pk>/offer/', OfferJobToWorkerView.as_view(), name='job-post-offer'),
]

