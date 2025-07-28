from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Count, Q
from django.utils import timezone
from .models import ServiceCategory, Service, ServiceInquiry
from .serializers import (
    ServiceCategorySerializer,
    ServiceListSerializer,
    ServiceDetailSerializer,
    ServiceInquirySerializer,
    ServiceInquiryAdminSerializer
)


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para las categorías de servicios"""
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            services_count=Count('services', filter=Q(services__is_active=True))
        )
        return queryset.order_by('order', 'name')


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para los servicios"""
    serializer_class = ServiceListSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'provider_name']
    ordering_fields = ['name', 'created_at', 'order', 'price_min']
    ordering = ['-is_featured', 'order', 'name']
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).select_related('category')
        
        # Filtro por categoría
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filtro por tipo de precio
        price_type = self.request.query_params.get('price_type')
        if price_type:
            queryset = queryset.filter(price_type=price_type)
        
        # Filtro por destacados
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Filtro por rango de precio
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        if price_min:
            queryset = queryset.filter(price_min__gte=price_min)
        if price_max:
            queryset = queryset.filter(price_max__lte=price_max)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        return ServiceListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Obtener detalles de un servicio e incrementar las vistas"""
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Obtener servicios destacados"""
        queryset = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Obtener servicios agrupados por categoría"""
        categories = ServiceCategory.objects.filter(is_active=True).prefetch_related(
            'services'
        ).annotate(
            services_count=Count('services', filter=Q(services__is_active=True))
        ).order_by('order', 'name')
        
        result = []
        for category in categories:
            if category.services_count > 0:
                services = category.services.filter(is_active=True).order_by('order', 'name')[:4]
                result.append({
                    'category': ServiceCategorySerializer(category).data,
                    'services': ServiceListSerializer(services, many=True).data
                })
        
        return Response(result)


class ServiceInquiryViewSet(viewsets.ModelViewSet):
    """ViewSet para las consultas de servicios"""
    serializer_class = ServiceInquirySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ServiceInquiry.objects.all().select_related('service', 'answered_by')
        return ServiceInquiry.objects.none()
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ServiceInquiryAdminSerializer
        return ServiceInquirySerializer
    
    def create(self, request, *args, **kwargs):
        """Crear una nueva consulta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Tu consulta ha sido enviada correctamente. Te contactaremos pronto.'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def mark_read(self, request, pk=None):
        """Marcar una consulta como leída"""
        inquiry = self.get_object()
        inquiry.is_read = True
        inquiry.save(update_fields=['is_read'])
        return Response({'status': 'marked as read'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def mark_answered(self, request, pk=None):
        """Marcar una consulta como respondida"""
        inquiry = self.get_object()
        inquiry.is_answered = True
        inquiry.answered_at = timezone.now()
        inquiry.answered_by = request.user
        inquiry.notes = request.data.get('notes', '')
        inquiry.save(update_fields=['is_answered', 'answered_at', 'answered_by', 'notes'])
        return Response({'status': 'marked as answered'})