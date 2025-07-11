from rest_framework import serializers
from .models import NewsPost
from apps.authentication.serializers import UserSerializer


class NewsListSerializer(serializers.ModelSerializer):
    """Serializer for news list view with basic information."""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    header_image_url = serializers.SerializerMethodField()
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = NewsPost
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'category',
            'header_image_url',
            'author_name',
            'views',
            'created_at',
            'url',
            'featured'
        ]
    
    def get_header_image_url(self, obj):
        if obj.header_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.header_image.url)
            return obj.header_image.url
        return None


class NewsDetailSerializer(serializers.ModelSerializer):
    """Serializer for news detail view with full content."""
    author = UserSerializer(read_only=True)
    header_image_url = serializers.SerializerMethodField()
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = NewsPost
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'excerpt',
            'category',
            'header_image_url',
            'author',
            'views',
            'created_at',
            'updated_at',
            'url',
            'featured'
        ]
    
    def get_header_image_url(self, obj):
        if obj.header_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.header_image.url)
            return obj.header_image.url
        return None


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating news posts."""
    
    class Meta:
        model = NewsPost
        fields = [
            'title',
            'content',
            'excerpt',
            'category',
            'header_image',
            'published',
            'featured'
        ]
    
    def validate_header_image(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("La imagen no debe superar los 5MB.")
        return value