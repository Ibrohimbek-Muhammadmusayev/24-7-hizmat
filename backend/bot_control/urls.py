from django.urls import path
from .views import (
    BotStatusView,
    BotStartView,
    BotStopView,
    BotRestartView,
    BotUpdateTokenView,
    BotUpdateSettingsView,
    BotSendMessageView,
    BroadcastMessageView
)

urlpatterns = [
    path('status/', BotStatusView.as_view(), name='bot-status'),
    path('start/', BotStartView.as_view(), name='bot-start'),
    path('stop/', BotStopView.as_view(), name='bot-stop'),
    path('restart/', BotRestartView.as_view(), name='bot-restart'),
    path('token/', BotUpdateTokenView.as_view(), name='bot-update-token'),
    path('settings/', BotUpdateSettingsView.as_view(), name='bot-update-settings'),
    path('send-message/', BotSendMessageView.as_view(), name='bot-send-message'),
    path('broadcast/', BroadcastMessageView.as_view(), name='bot-broadcast'),
]
