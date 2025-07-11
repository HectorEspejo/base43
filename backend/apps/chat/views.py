from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Max
from django.utils import timezone
from .models import Channel, Message, ChannelMembership
from .serializers import (
    ChannelSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    ChannelMembershipSerializer,
    FileUploadSerializer
)


class ChannelListView(generics.ListAPIView):
    """List all active channels with unread counts."""
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Channel.objects.filter(is_active=True).annotate(
            last_message_time=Max('messages__created_at')
        ).order_by('-last_message_time', 'name')


class ChannelDetailView(generics.RetrieveAPIView):
    """Get channel details."""
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Channel.objects.filter(is_active=True)


class ChannelMessagesView(generics.ListAPIView):
    """List messages for a specific channel."""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        channel_id = self.kwargs.get('channel_id')
        channel = get_object_or_404(Channel, id=channel_id, is_active=True)
        
        # Update membership last read
        membership, created = ChannelMembership.objects.get_or_create(
            user=self.request.user,
            channel=channel
        )
        membership.mark_as_read()
        
        # Get messages
        return Message.objects.filter(
            channel=channel
        ).select_related('user').order_by('-created_at')[:100]  # Last 100 messages
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Reverse the order to show oldest first
        response.data['results'] = list(reversed(response.data['results']))
        return response


class MessageCreateView(generics.CreateAPIView):
    """Create a new message."""
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        message = serializer.save()
        
        # Update membership
        membership, created = ChannelMembership.objects.get_or_create(
            user=self.request.user,
            channel=message.channel
        )
        membership.mark_as_read()


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update or delete a message."""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        # Users can only update/delete their own messages
        return Message.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(edited_at=timezone.now())
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.soft_delete()


class FileUploadView(APIView):
    """Handle file uploads for chat."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            
            # Return file info without saving
            # The actual saving will be done when creating the message
            return Response({
                'name': file.name,
                'size': file.size,
                'type': 'image' if file.name.split('.')[-1].lower() in ['png', 'jpg', 'jpeg', 'gif'] else 'document'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnlineUsersView(APIView):
    """Get list of online users."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # This is a placeholder - in production you'd track this via WebSocket connections
        # For now, return empty list
        return Response([])


class UserChannelsView(generics.ListAPIView):
    """Get user's channel memberships with unread counts."""
    serializer_class = ChannelMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ChannelMembership.objects.filter(
            user=self.request.user,
            channel__is_active=True
        ).select_related('channel')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_channel_as_read(request, channel_id):
    """Mark all messages in a channel as read."""
    channel = get_object_or_404(Channel, id=channel_id, is_active=True)
    
    membership, created = ChannelMembership.objects.get_or_create(
        user=request.user,
        channel=channel
    )
    membership.mark_as_read()
    
    return Response({'status': 'success'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_messages(request):
    """Search messages across all channels."""
    query = request.GET.get('q', '')
    
    if not query:
        return Response({'results': []})
    
    messages = Message.objects.filter(
        Q(content__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query),
        channel__is_active=True,
        is_deleted=False
    ).select_related('user', 'channel').order_by('-created_at')[:50]
    
    serializer = MessageSerializer(messages, many=True, context={'request': request})
    return Response({'results': serializer.data})