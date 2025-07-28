from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Count, Q
from .models import PartnerCategory, Partner, PartnerTestimonial, PartnerProject
from .serializers import (
    PartnerCategorySerializer,
    PartnerListSerializer,
    PartnerDetailSerializer,
    PartnerCreateUpdateSerializer,
    PartnerTestimonialSerializer,
    PartnerProjectSerializer
)


class PartnerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para las categorías de partners"""
    queryset = PartnerCategory.objects.filter(is_active=True)
    serializer_class = PartnerCategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            partners_count=Count('partners', filter=Q(partners__is_active=True))
        )
        return queryset.order_by('order', 'name')


class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para los partners"""
    serializer_class = PartnerListSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'province', 'description', 'mission']
    ordering_fields = ['name', 'created_at', 'collaboration_start', 'order']
    ordering = ['-is_featured', 'order', 'name']
    
    def get_queryset(self):
        queryset = Partner.objects.filter(is_active=True).select_related('category')
        
        # Filtro por categoría
        category = self.request.query_params.get('category')
        if category and category != 'todos':
            queryset = queryset.filter(category__slug=category)
        
        # Filtro por tipo de partner
        partner_type = self.request.query_params.get('partner_type')
        if partner_type:
            queryset = queryset.filter(partner_type=partner_type)
        
        # Filtro por ciudad
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Filtro por provincia
        province = self.request.query_params.get('province')
        if province:
            queryset = queryset.filter(province__icontains=province)
        
        # Filtro por destacados
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Filtro por área de colaboración
        collaboration_area = self.request.query_params.get('collaboration_area')
        if collaboration_area:
            queryset = queryset.filter(collaboration_areas__icontains=collaboration_area)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PartnerDetailSerializer
        return PartnerListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Obtener detalles de un partner"""
        instance = self.get_object()
        
        # Prefetch related para optimizar queries
        instance = Partner.objects.prefetch_related(
            'testimonials',
            'partner_projects__project'
        ).get(pk=instance.pk)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Obtener partners destacados"""
        queryset = self.get_queryset().filter(is_featured=True)[:8]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Obtener partners agrupados por tipo"""
        result = {}
        
        for partner_type, label in Partner.PARTNER_TYPES:
            partners = self.get_queryset().filter(partner_type=partner_type)[:4]
            if partners:
                result[partner_type] = {
                    'label': label,
                    'partners': PartnerListSerializer(partners, many=True).data
                }
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def locations(self, request):
        """Obtener lista de ubicaciones disponibles"""
        queryset = self.get_queryset()
        cities = queryset.values_list('city', flat=True).distinct().order_by('city')
        provinces = queryset.values_list('province', flat=True).distinct().order_by('province')
        
        return Response({
            'cities': list(cities),
            'provinces': list(provinces)
        })
    
    @action(detail=False, methods=['get'])
    def collaboration_areas(self, request):
        """Obtener áreas de colaboración únicas"""
        queryset = self.get_queryset()
        areas = set()
        
        for partner in queryset:
            areas.update(partner.get_collaboration_areas_list())
        
        return Response({
            'areas': sorted(list(areas))
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtener estadísticas generales de partners"""
        queryset = self.get_queryset()
        
        stats = {
            'total_partners': queryset.count(),
            'by_type': {},
            'by_category': {},
            'featured_count': queryset.filter(is_featured=True).count(),
            'with_testimonials': queryset.filter(testimonials__is_active=True).distinct().count()
        }
        
        # Por tipo
        for partner_type, label in Partner.PARTNER_TYPES:
            count = queryset.filter(partner_type=partner_type).count()
            if count > 0:
                stats['by_type'][partner_type] = {
                    'label': label,
                    'count': count
                }
        
        # Por categoría
        categories = PartnerCategory.objects.filter(is_active=True).annotate(
            count=Count('partners', filter=Q(partners__is_active=True))
        )
        for cat in categories:
            if cat.count > 0:
                stats['by_category'][cat.slug] = {
                    'name': cat.name,
                    'count': cat.count
                }
        
        return Response(stats)
    
    @action(detail=True, methods=['get'])
    def projects(self, request, slug=None):
        """Obtener proyectos de un partner específico"""
        partner = self.get_object()
        projects = partner.partner_projects.filter(is_active=True).select_related('project')
        serializer = PartnerProjectSerializer(projects, many=True)
        return Response(serializer.data)


class PartnerTestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para los testimonios de partners"""
    serializer_class = PartnerTestimonialSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = PartnerTestimonial.objects.filter(is_active=True)
        
        # Filtro por partner
        partner_slug = self.request.query_params.get('partner')
        if partner_slug:
            queryset = queryset.filter(partner__slug=partner_slug)
        
        return queryset.select_related('partner').order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obtener testimonios recientes"""
        queryset = self.get_queryset()[:6]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)