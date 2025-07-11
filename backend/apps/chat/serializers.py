from rest_framework import serializers
from .models import Channel, Message, ChannelMembership
from apps.authentication.serializers import UserSerializer


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for chat channels."""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    member_count = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Channel
        fields = [
            'id', 'name', 'description', 'created_by', 'created_by_name',
            'created_at', 'is_active', 'member_count', 'unread_count'
        ]
        read_only_fields = ['created_by', 'created_at']
    
    def get_member_count(self, obj):
        return obj.get_member_count()
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                membership = ChannelMembership.objects.get(
                    user=request.user,
                    channel=obj
                )
                return membership.get_unread_count()
            except ChannelMembership.DoesNotExist:
                return 0
        return 0


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages."""
    user = UserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'channel', 'user', 'content', 'file', 'file_url',
            'file_type', 'file_name', 'created_at', 'edited_at', 'is_deleted'
        ]
        read_only_fields = ['created_at', 'edited_at', 'file_type', 'file_name']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating messages."""
    
    class Meta:
        model = Message
        fields = ['channel', 'content', 'file']
    
    def validate(self, data):
        if not data.get('content') and not data.get('file'):
            raise serializers.ValidationError(
                "El mensaje debe contener texto o un archivo."
            )
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ChannelMembershipSerializer(serializers.ModelSerializer):
    """Serializer for channel memberships."""
    channel = ChannelSerializer(read_only=True)
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChannelMembership
        fields = ['id', 'channel', 'last_read_at', 'joined_at', 'unread_count']
        read_only_fields = ['joined_at']
    
    def get_unread_count(self, obj):
        return obj.get_unread_count()


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file uploads."""
    file = serializers.FileField()
    
    def validate_file(self, value):
        # Check file size
        if value.size > 20 * 1024 * 1024:  # 20MB
            raise serializers.ValidationError("El archivo no puede superar los 20MB.")
        
        # Check file extension
        ext = value.name.split('.')[-1].lower()
        allowed_extensions = ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'xlsx', 'doc', 'xls']
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(allowed_extensions)}"
            )
        
        return value