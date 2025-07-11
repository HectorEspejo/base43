import json
import base64
import markdown2
import bleach
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import Channel, Message, ChannelMembership
from apps.authentication.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time chat."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.user = self.scope["user"]
        
        # Check if user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.channel_groups = []
        
        # Accept the connection
        await self.accept()
        
        # Get all channels and add user to groups
        channels = await self.get_all_channels()
        for channel in channels:
            group_name = f"chat_{channel.id}"
            self.channel_groups.append(group_name)
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )
        
        # Add user to online users group
        await self.channel_layer.group_add(
            "online_users",
            self.channel_name
        )
        
        # Notify others that user is online
        await self.channel_layer.group_send(
            "online_users",
            {
                "type": "user_online",
                "user_id": self.user.id,
                "user_name": self.user.get_full_name(),
                "user_avatar": self.user.avatar.url if self.user.avatar else None
            }
        )
        
        # Send initial data
        await self.send_initial_data()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if hasattr(self, 'user') and self.user.is_authenticated:
            # Remove from all channel groups
            for group_name in self.channel_groups:
                await self.channel_layer.group_discard(
                    group_name,
                    self.channel_name
                )
            
            # Remove from online users
            await self.channel_layer.group_discard(
                "online_users",
                self.channel_name
            )
            
            # Notify others that user is offline
            await self.channel_layer.group_send(
                "online_users",
                {
                    "type": "user_offline",
                    "user_id": self.user.id
                }
            )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'send_message':
                await self.handle_send_message(data)
            elif message_type == 'mark_as_read':
                await self.handle_mark_as_read(data)
            elif message_type == 'typing':
                await self.handle_typing(data)
            elif message_type == 'delete_message':
                await self.handle_delete_message(data)
            
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON")
        except Exception as e:
            await self.send_error(str(e))
    
    async def handle_send_message(self, data):
        """Handle sending a new message."""
        channel_id = data.get('channel_id')
        content = data.get('content', '').strip()
        file_data = data.get('file')
        
        if not channel_id or (not content and not file_data):
            await self.send_error("Canal y contenido/archivo requeridos")
            return
        
        # Sanitize content
        if content:
            # Convert markdown to HTML
            html_content = markdown2.markdown(
                content,
                extras=['fenced-code-blocks', 'tables', 'break-on-newline']
            )
            # Sanitize HTML
            allowed_tags = [
                'p', 'br', 'strong', 'em', 'u', 's', 'code', 'pre',
                'blockquote', 'ul', 'ol', 'li', 'a', 'img', 'table',
                'thead', 'tbody', 'tr', 'th', 'td', 'h1', 'h2', 'h3',
                'h4', 'h5', 'h6'
            ]
            allowed_attributes = {
                'a': ['href', 'title'],
                'img': ['src', 'alt', 'title'],
                'code': ['class']
            }
            content = bleach.clean(
                html_content,
                tags=allowed_tags,
                attributes=allowed_attributes,
                strip=True
            )
        
        # Create message
        message = await self.create_message(
            channel_id=channel_id,
            content=content,
            file_data=file_data
        )
        
        if message:
            # Prepare message data
            message_data = {
                "type": "new_message",
                "message": {
                    "id": message.id,
                    "channel_id": message.channel_id,
                    "user": {
                        "id": message.user.id,
                        "name": message.user.get_full_name(),
                        "avatar": message.user.avatar.url if message.user.avatar else None
                    },
                    "content": message.content,
                    "file": {
                        "url": message.get_file_url(),
                        "type": message.file_type,
                        "name": message.file_name
                    } if message.file else None,
                    "created_at": message.created_at.isoformat(),
                    "is_deleted": message.is_deleted
                }
            }
            
            # Send to channel group
            await self.channel_layer.group_send(
                f"chat_{channel_id}",
                message_data
            )
    
    async def handle_mark_as_read(self, data):
        """Handle marking channel as read."""
        channel_id = data.get('channel_id')
        
        if channel_id:
            await self.mark_channel_as_read(channel_id)
            
            # Send confirmation
            await self.send(text_data=json.dumps({
                "type": "marked_as_read",
                "channel_id": channel_id
            }))
    
    async def handle_typing(self, data):
        """Handle typing indicator."""
        channel_id = data.get('channel_id')
        is_typing = data.get('is_typing', False)
        
        if channel_id:
            await self.channel_layer.group_send(
                f"chat_{channel_id}",
                {
                    "type": "user_typing",
                    "user_id": self.user.id,
                    "user_name": self.user.get_full_name(),
                    "channel_id": channel_id,
                    "is_typing": is_typing
                }
            )
    
    async def handle_delete_message(self, data):
        """Handle message deletion."""
        message_id = data.get('message_id')
        
        if message_id:
            success = await self.delete_message(message_id)
            
            if success:
                # Notify channel
                message = await self.get_message(message_id)
                if message:
                    await self.channel_layer.group_send(
                        f"chat_{message.channel_id}",
                        {
                            "type": "message_deleted",
                            "message_id": message_id,
                            "channel_id": message.channel_id
                        }
                    )
    
    # WebSocket event handlers
    async def new_message(self, event):
        """Send new message to WebSocket."""
        await self.send(text_data=json.dumps(event))
    
    async def user_online(self, event):
        """Send user online notification."""
        await self.send(text_data=json.dumps(event))
    
    async def user_offline(self, event):
        """Send user offline notification."""
        await self.send(text_data=json.dumps(event))
    
    async def user_typing(self, event):
        """Send typing indicator."""
        # Don't send typing indicator to the user who is typing
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps(event))
    
    async def message_deleted(self, event):
        """Send message deletion notification."""
        await self.send(text_data=json.dumps(event))
    
    # Helper methods
    async def send_error(self, error_message):
        """Send error message to client."""
        await self.send(text_data=json.dumps({
            "type": "error",
            "message": error_message
        }))
    
    async def send_initial_data(self):
        """Send initial data when user connects."""
        channels = await self.get_channels_with_unread_count()
        online_users = await self.get_online_users()
        
        await self.send(text_data=json.dumps({
            "type": "initial_data",
            "channels": channels,
            "online_users": online_users,
            "current_user": {
                "id": self.user.id,
                "name": self.user.get_full_name(),
                "avatar": self.user.avatar.url if self.user.avatar else None
            }
        }))
    
    # Database operations
    @database_sync_to_async
    def get_all_channels(self):
        """Get all active channels."""
        return list(Channel.objects.filter(is_active=True))
    
    @database_sync_to_async
    def get_channels_with_unread_count(self):
        """Get channels with unread count for user."""
        channels = []
        for channel in Channel.objects.filter(is_active=True):
            membership, created = ChannelMembership.objects.get_or_create(
                user=self.user,
                channel=channel
            )
            channels.append({
                "id": channel.id,
                "name": channel.name,
                "description": channel.description,
                "unread_count": membership.get_unread_count()
            })
        return channels
    
    @database_sync_to_async
    def get_online_users(self):
        """Get list of online users."""
        # This is a simplified version - in production you'd track this properly
        return []
    
    @database_sync_to_async
    def create_message(self, channel_id, content, file_data=None):
        """Create a new message."""
        try:
            channel = Channel.objects.get(id=channel_id, is_active=True)
            
            message = Message(
                channel=channel,
                user=self.user,
                content=content
            )
            
            # Handle file upload
            if file_data:
                file_content = base64.b64decode(file_data['content'])
                file_name = file_data['name']
                message.file.save(file_name, ContentFile(file_content))
            
            message.save()
            
            # Update membership
            membership, created = ChannelMembership.objects.get_or_create(
                user=self.user,
                channel=channel
            )
            membership.mark_as_read()
            
            return message
        except Channel.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
    
    @database_sync_to_async
    def mark_channel_as_read(self, channel_id):
        """Mark channel as read for user."""
        try:
            membership = ChannelMembership.objects.get(
                user=self.user,
                channel_id=channel_id
            )
            membership.mark_as_read()
            return True
        except ChannelMembership.DoesNotExist:
            return False
    
    @database_sync_to_async
    def get_message(self, message_id):
        """Get a message by ID."""
        try:
            return Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return None
    
    @database_sync_to_async
    def delete_message(self, message_id):
        """Soft delete a message."""
        try:
            message = Message.objects.get(id=message_id, user=self.user)
            message.soft_delete()
            return True
        except Message.DoesNotExist:
            return False