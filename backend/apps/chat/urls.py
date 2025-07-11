from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Channels
    path('channels/', views.ChannelListView.as_view(), name='channel-list'),
    path('channels/<int:id>/', views.ChannelDetailView.as_view(), name='channel-detail'),
    path('channels/<int:channel_id>/messages/', views.ChannelMessagesView.as_view(), name='channel-messages'),
    path('channels/<int:channel_id>/mark-read/', views.mark_channel_as_read, name='mark-channel-read'),
    
    # Messages
    path('messages/', views.MessageCreateView.as_view(), name='message-create'),
    path('messages/<int:id>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('messages/search/', views.search_messages, name='message-search'),
    
    # File upload
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    
    # Users
    path('online-users/', views.OnlineUsersView.as_view(), name='online-users'),
    path('my-channels/', views.UserChannelsView.as_view(), name='user-channels'),
]