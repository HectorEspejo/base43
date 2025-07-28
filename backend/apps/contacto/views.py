# -*- coding: utf-8 -*-
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from .models import ContactMessage
from .serializers import ContactMessageSerializer, ContactMessageListSerializer


class ContactMessageCreateView(generics.CreateAPIView):
    """
    Public endpoint to submit contact messages
    """
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        # Send email notification to admin (optional)
        try:
            self.send_admin_notification(message)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error sending email notification: {e}")
        
        return Response({
            'success': True,
            'message': 'Tu mensaje ha sido enviado correctamente. Te responderemos lo antes posible.'
        }, status=status.HTTP_201_CREATED)
    
    def send_admin_notification(self, message):
        """Send email notification to admin when new message is received"""
        subject = f'Nuevo mensaje de contacto: {message.get_subject_display()}'
        email_message = f"""
        Nuevo mensaje recibido a través del formulario de contacto:
        
        De: {message.full_name}
        Email: {message.email}
        Teléfono: {message.phone or 'No proporcionado'}
        Asunto: {message.get_subject_display()}
        
        Mensaje:
        {message.message}
        
        ---
        Fecha: {message.created_at.strftime('%d/%m/%Y %H:%M')}
        IP: {message.ip_address or 'No disponible'}
        """
        
        # Send to admin email(s)
        admin_emails = getattr(settings, 'CONTACT_ADMIN_EMAILS', ['calicanto.habitat@adobeverde.eu'])
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            admin_emails,
            fail_silently=True,
        )


class ContactMessageListView(generics.ListAPIView):
    """
    Admin endpoint to list all contact messages
    """
    serializer_class = ContactMessageListSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by subject
        subject_filter = self.request.query_params.get('subject', None)
        if subject_filter:
            queryset = queryset.filter(subject=subject_filter)
        
        # Search by name or email
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(surname__icontains=search) |
                models.Q(email__icontains=search)
            )
        
        return queryset


class ContactMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin endpoint to view, update or delete a contact message
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageListSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark as read when viewed
        instance.mark_as_read()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def mark_message_as_answered(request, pk):
    """
    Mark a message as answered
    """
    try:
        message = ContactMessage.objects.get(pk=pk)
        message.status = 'answered'
        message.save()
        return Response({
            'success': True,
            'message': 'Mensaje marcado como respondido'
        })
    except ContactMessage.DoesNotExist:
        return Response({
            'error': 'Mensaje no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def contact_stats(request):
    """
    Get contact message statistics
    """
    from django.db.models import Count
    
    stats = {
        'total': ContactMessage.objects.count(),
        'new': ContactMessage.objects.filter(status='new').count(),
        'read': ContactMessage.objects.filter(status='read').count(),
        'answered': ContactMessage.objects.filter(status='answered').count(),
        'by_subject': list(
            ContactMessage.objects.values('subject').annotate(
                count=Count('id')
            ).order_by('-count')
        )
    }
    
    return Response(stats)