from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q

from .models import Resource, ResourceCategory, ResourceImage, ResourceDocument
from .serializers import (
    ResourceListSerializer,
    ResourceDetailSerializer,
    ResourceCreateUpdateSerializer,
    ResourceMapSerializer,
    ResourceCategorySerializer,
    ResourceImageSerializer,
    ResourceDocumentSerializer
)


class ResourceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para las categorías de recursos (solo lectura)"""
    queryset = ResourceCategory.objects.all()
    serializer_class = ResourceCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # Disable pagination for categories


class ResourceViewSet(viewsets.ModelViewSet):
    """ViewSet principal para los recursos"""
    queryset = Resource.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Campos para búsqueda
    search_fields = ['name', 'description', 'address', 'services']
    
    # Campos para ordenamiento
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-is_featured', 'name']
    
    def get_serializer_class(self):
        """Devuelve el serializer apropiado según la acción"""
        if self.action == 'list':
            return ResourceListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ResourceCreateUpdateSerializer
        elif self.action == 'map':
            return ResourceMapSerializer
        return ResourceDetailSerializer
    
    def get_queryset(self):
        """Personaliza el queryset según los parámetros"""
        queryset = super().get_queryset()
        
        # Incluye relaciones para optimizar consultas
        if self.action == 'list':
            queryset = queryset.select_related('category')
        elif self.action == 'retrieve':
            queryset = queryset.select_related('category', 'created_by').prefetch_related('images', 'documents')
        
        # Filtros manuales
        type_filter = self.request.query_params.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        
        city_filter = self.request.query_params.get('city')
        if city_filter:
            queryset = queryset.filter(city=city_filter)
        
        category_filter = self.request.query_params.get('category')
        if category_filter:
            queryset = queryset.filter(category_id=category_filter)
        
        featured_filter = self.request.query_params.get('is_featured')
        if featured_filter is not None:
            queryset = queryset.filter(is_featured=featured_filter.lower() == 'true')
        
        # Filtro adicional por múltiples categorías
        categories = self.request.query_params.getlist('categories[]')
        if categories:
            queryset = queryset.filter(category__id__in=categories)
        
        # Filtro por coordenadas (para búsquedas por área)
        lat_min = self.request.query_params.get('lat_min')
        lat_max = self.request.query_params.get('lat_max')
        lng_min = self.request.query_params.get('lng_min')
        lng_max = self.request.query_params.get('lng_max')
        
        if all([lat_min, lat_max, lng_min, lng_max]):
            queryset = queryset.filter(
                latitude__gte=lat_min,
                latitude__lte=lat_max,
                longitude__gte=lng_min,
                longitude__lte=lng_max
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def map(self, request):
        """Endpoint optimizado para obtener recursos para el mapa"""
        queryset = self.filter_queryset(self.get_queryset())
        # Solo devuelve recursos con coordenadas
        queryset = queryset.exclude(
            Q(latitude__isnull=True) | Q(longitude__isnull=True)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Obtiene solo los recursos destacados"""
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = ResourceListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def cities(self, request):
        """Obtiene las ciudades disponibles con conteo de recursos"""
        from django.db.models import Count
        cities_data = []
        
        # Get unique cities with their counts
        cities = self.get_queryset().values('city').annotate(count=Count('city')).order_by('city')
        
        for city_info in cities:
            if city_info['city']:  # Skip empty cities
                cities_data.append({
                    'code': city_info['city'].lower().replace(' ', '_'),
                    'name': city_info['city'],
                    'count': city_info['count']
                })
        
        return Response(cities_data)
    
    @action(detail=False, methods=['get'])
    def types(self, request):
        """Obtiene los tipos disponibles con conteo de recursos"""
        types_data = []
        for type_code, type_name in Resource.RESOURCE_TYPES:
            count = self.get_queryset().filter(type=type_code).count()
            if count > 0:
                types_data.append({
                    'code': type_code,
                    'name': type_name,
                    'count': count
                })
        return Response(types_data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_image(self, request, pk=None):
        """Añade una imagen a un recurso"""
        resource = self.get_object()
        serializer = ResourceImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(resource=resource)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_document(self, request, pk=None):
        """Añade un documento a un recurso"""
        resource = self.get_object()
        serializer = ResourceDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(resource=resource)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)