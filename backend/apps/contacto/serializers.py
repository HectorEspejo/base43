# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for creating contact messages from the public form
    """
    privacy = serializers.BooleanField(write_only=True, required=True)
    
    class Meta:
        model = ContactMessage
        fields = [
            'name', 'surname', 'email', 'phone', 
            'subject', 'message', 'privacy'
        ]
    
    def validate_privacy(self, value):
        if not value:
            raise serializers.ValidationError(
                "Debe aceptar la política de privacidad."
            )
        return value
    
    def create(self, validated_data):
        # Remove privacy field as it's not in the model
        validated_data.pop('privacy', None)
        
        # Add metadata from request if available
        request = self.context.get('request')
        if request:
            validated_data['ip_address'] = self.get_client_ip(request)
            validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
            
            # If user is authenticated, link the message to the user
            if request.user.is_authenticated:
                validated_data['user'] = request.user
        
        return super().create(validated_data)
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ContactMessageListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing contact messages (admin view)
    """
    full_name = serializers.ReadOnlyField()
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'full_name', 'email', 'phone',
            'subject', 'subject_display', 'message',
            'status', 'status_display', 'created_at',
            'is_new', 'user'
        ]