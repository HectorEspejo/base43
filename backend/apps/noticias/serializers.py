from rest_framework import serializers
from django.utils.html import format_html
from bs4 import BeautifulSoup
import re
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
    content = serializers.SerializerMethodField()
    
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
    
    def get_content(self, obj):
        """Process content to make image URLs absolute."""
        content = obj.content
        request = self.context.get('request')
        
        if not request or not content:
            return content
        
        # Parse HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all img tags
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src and not src.startswith(('http://', 'https://', '//')):
                # Convert relative URL to absolute
                if src.startswith('/'):
                    img['src'] = request.build_absolute_uri(src)
                else:
                    img['src'] = request.build_absolute_uri('/media/' + src)
        
        # Find all links that might be images
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href and href.startswith('/media/'):
                link['href'] = request.build_absolute_uri(href)
        
        return str(soup)


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