"""
Base views for Base43 project.
Provides common viewsets and mixins for API views.
"""
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that provides standard CRUD operations
    with common features like filtering, searching, and pagination.
    """
    search_fields = []
    filterset_fields = []
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """
        Save the user who created the object.
        """
        if hasattr(serializer.Meta.model, 'created_by'):
            serializer.save(created_by=self.request.user)
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        """
        Save the user who updated the object.
        """
        if hasattr(serializer.Meta.model, 'updated_by'):
            serializer.save(updated_by=self.request.user)
        else:
            serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Create a new instance with standardized response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': f'{self.get_serializer().Meta.model.__name__} created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """
        Update an instance with standardized response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'success': True,
            'message': f'{self.get_serializer().Meta.model.__name__} updated successfully',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete an instance with standardized response.
        """
        instance = self.get_object()
        
        # Check if model supports soft delete
        if hasattr(instance, 'is_deleted'):
            instance.delete(soft=True, deleted_by=request.user)
            message = f'{self.get_serializer().Meta.model.__name__} deleted successfully'
        else:
            self.perform_destroy(instance)
            message = f'{self.get_serializer().Meta.model.__name__} permanently deleted'
        
        return Response({
            'success': True,
            'message': message
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get statistics about the model.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        stats = {
            'total': queryset.count(),
            'created_today': queryset.filter(
                created_at__date=timezone.now().date()
            ).count() if hasattr(self.get_serializer().Meta.model, 'created_at') else 0
        }
        
        return Response(stats)


class PublishableViewSetMixin:
    """
    Mixin for viewsets that work with publishable models.
    """
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        """
        Publish an item.
        """
        instance = self.get_object()
        instance.publish()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Published successfully',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unpublish(self, request, pk=None):
        """
        Unpublish an item.
        """
        instance = self.get_object()
        instance.unpublish()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Unpublished successfully',
            'data': serializer.data
        })
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        """
        queryset = super().get_queryset()
        
        # Non-authenticated users only see published items
        if not self.request.user.is_authenticated:
            if hasattr(queryset.model, 'is_published'):
                queryset = queryset.filter(is_published=True)
        
        return queryset


class BulkOperationsMixin:
    """
    Mixin that adds bulk operations to viewsets.
    """
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def bulk_delete(self, request):
        """
        Bulk delete multiple items.
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response({
                'success': False,
                'message': 'No IDs provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(id__in=ids)
        count = queryset.count()
        
        # Soft delete if supported, otherwise hard delete
        if hasattr(queryset.model, 'is_deleted'):
            queryset.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=request.user
            )
        else:
            queryset.delete()
        
        return Response({
            'success': True,
            'message': f'{count} items deleted successfully'
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def bulk_update(self, request):
        """
        Bulk update multiple items.
        """
        ids = request.data.get('ids', [])
        updates = request.data.get('updates', {})
        
        if not ids or not updates:
            return Response({
                'success': False,
                'message': 'IDs and updates are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(id__in=ids)
        count = queryset.count()
        
        # Add updated_by if model supports it
        if hasattr(queryset.model, 'updated_by'):
            updates['updated_by'] = request.user
        
        queryset.update(**updates)
        
        return Response({
            'success': True,
            'message': f'{count} items updated successfully'
        })


class SearchableViewSetMixin:
    """
    Mixin that adds advanced search capabilities.
    """
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search endpoint.
        """
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({
                'success': False,
                'message': 'Search query is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Build Q objects for searching across multiple fields
        search_fields = getattr(self, 'search_fields', [])
        
        if not search_fields:
            return Response({
                'success': False,
                'message': 'Search not configured for this endpoint'
            }, status=status.HTTP_501_NOT_IMPLEMENTED)
        
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f'{field}__icontains': query})
        
        queryset = self.filter_queryset(self.get_queryset()).filter(q_objects)
        
        # Paginate results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'results': serializer.data,
            'count': len(serializer.data)
        })


class ExportMixin:
    """
    Mixin that adds data export functionality.
    """
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def export(self, request):
        """
        Export data in various formats.
        """
        format_type = request.query_params.get('format', 'json').lower()
        
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        if format_type == 'csv':
            import csv
            from django.http import HttpResponse
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{self.basename}_export.csv"'
            
            if serializer.data:
                writer = csv.DictWriter(response, fieldnames=serializer.data[0].keys())
                writer.writeheader()
                writer.writerows(serializer.data)
            
            return response
        
        else:  # Default to JSON
            return Response({
                'success': True,
                'data': serializer.data,
                'count': len(serializer.data),
                'exported_at': timezone.now()
            })


# Combined viewset with all common functionality
class FullFeaturedModelViewSet(
    BaseModelViewSet,
    PublishableViewSetMixin,
    BulkOperationsMixin,
    SearchableViewSetMixin,
    ExportMixin
):
    """
    A viewset that provides all common functionality:
    - Standard CRUD operations
    - Publishing/unpublishing
    - Bulk operations
    - Advanced search
    - Data export
    """
    pass