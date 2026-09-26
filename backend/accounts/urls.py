from django.urls import path
from .views import (
    LoginView, 
    ChangeAdminCredentialsView,
    DownloadDatabaseBackupView,
    UserProfileView, 
    ToggleOnlineView, 
    UpdateFCMTokenView, 
    WorkerListView, 
    WorkerDetailView,
    RegisterWorkerView,
    UserListView,
    UserDetailView,
    UpdateUserCreditsView,
    RequestProfileUpdateView,
    UserFeedbackListView,
    UserFeedbackDetailView,
    LeadsListView,
    SendLeadReminderView,
    DeleteLeadView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('change-credentials/', ChangeAdminCredentialsView.as_view(), name='change-credentials'),
    path('download-backup/', DownloadDatabaseBackupView.as_view(), name='download-backup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('toggle-online/', ToggleOnlineView.as_view(), name='toggle-online'),
    path('fcm-token/', UpdateFCMTokenView.as_view(), name='fcm-token'),
    path('workers/', WorkerListView.as_view(), name='worker-list'),
    path('workers/<int:pk>/', WorkerDetailView.as_view(), name='worker-detail'),
    path('register-worker/', RegisterWorkerView.as_view(), name='register-worker'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/credits/', UpdateUserCreditsView.as_view(), name='update-user-credits'),
    path('users/<int:user_id>/request-profile-update/', RequestProfileUpdateView.as_view(), name='request-profile-update'),
    path('feedbacks/', UserFeedbackListView.as_view(), name='feedback-list'),
    path('feedbacks/<int:pk>/', UserFeedbackDetailView.as_view(), name='feedback-detail'),
    path('leads/', LeadsListView.as_view(), name='leads-list'),
    path('leads/send-reminder/', SendLeadReminderView.as_view(), name='leads-send-reminder'),
    path('leads/<int:pk>/', DeleteLeadView.as_view(), name='lead-delete'),
]


