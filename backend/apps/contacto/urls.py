from django.urls import path
from .views import (
    ContactMessageCreateView,
    ContactMessageListView,
    ContactMessageDetailView,
    mark_message_as_answered,
    contact_stats
)

app_name = 'contacto'

urlpatterns = [
    # Public endpoint
    path('send/', ContactMessageCreateView.as_view(), name='send_message'),
    
    # Admin endpoints
    path('messages/', ContactMessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', ContactMessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/answer/', mark_message_as_answered, name='mark_answered'),
    path('stats/', contact_stats, name='contact_stats'),
]