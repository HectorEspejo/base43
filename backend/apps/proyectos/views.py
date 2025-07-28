from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Count, Q, Prefetch
from django.utils import timezone
from .models import ProjectCategory, Project, ProjectImage, ProjectUpdate
from .serializers import (
    ProjectCategorySerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectCreateUpdateSerializer,
    ProjectImageSerializer,
    ProjectUpdateSerializer
)


class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para las categorías de proyectos"""
    queryset = ProjectCategory.objects.filter(is_active=True)
    serializer_class = ProjectCategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            projects_count=Count('projects', filter=Q(projects__is_active=True))
        )
        return queryset.order_by('order', 'name')


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para los proyectos"""
    serializer_class = ProjectListSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'province', 'description']
    ordering_fields = ['name', 'created_at', 'start_date', 'units', 'participants']
    ordering = ['-is_featured', 'order', '-created_at']
    
    def get_queryset(self):
        queryset = Project.objects.filter(is_active=True).select_related('category')
        
        # Filtro por categoría
        category = self.request.query_params.get('category')
        if category and category != 'todos':
            queryset = queryset.filter(category__slug=category)
        
        # Filtro por estado
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
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
        
        # Filtro por rango de unidades
        units_min = self.request.query_params.get('units_min')
        units_max = self.request.query_params.get('units_max')
        if units_min:
            queryset = queryset.filter(units__gte=units_min)
        if units_max:
            queryset = queryset.filter(units__lte=units_max)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Obtener detalles de un proyecto e incrementar las vistas"""
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        
        # Prefetch related para optimizar queries
        instance = Project.objects.prefetch_related(
            'images',
            'documents',
            'updates'
        ).get(pk=instance.pk)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Obtener proyectos destacados"""
        queryset = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Obtener proyectos agrupados por estado"""
        result = {}
        statuses = ['planning', 'development', 'construction', 'active']
        
        for status in statuses:
            projects = self.get_queryset().filter(status=status)[:4]
            if projects:
                result[status] = ProjectListSerializer(projects, many=True).data
        
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
    def statistics(self, request):
        """Obtener estadísticas generales de proyectos"""
        queryset = self.get_queryset()
        
        stats = {
            'total_projects': queryset.count(),
            'total_units': sum(queryset.values_list('units', flat=True)),
            'total_participants': sum(queryset.values_list('participants', flat=True)),
            'by_status': {},
            'by_category': {}
        }
        
        # Por estado
        for status, label in Project.STATUS_CHOICES:
            count = queryset.filter(status=status).count()
            if count > 0:
                stats['by_status'][status] = {
                    'label': label,
                    'count': count
                }
        
        # Por categoría
        categories = ProjectCategory.objects.filter(is_active=True).annotate(
            count=Count('projects', filter=Q(projects__is_active=True))
        )
        for cat in categories:
            if cat.count > 0:
                stats['by_category'][cat.slug] = {
                    'name': cat.name,
                    'count': cat.count
                }
        
        return Response(stats)


class ProjectImageViewSet(viewsets.ModelViewSet):
    """ViewSet para las imágenes de proyectos"""
    serializer_class = ProjectImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        project_slug = self.kwargs.get('project_slug')
        return ProjectImage.objects.filter(
            project__slug=project_slug
        ).order_by('order', 'created_at')


class ProjectUpdateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para las actualizaciones de proyectos"""
    serializer_class = ProjectUpdateSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        project_slug = self.kwargs.get('project_slug')
        if project_slug:
            return ProjectUpdate.objects.filter(
                project__slug=project_slug,
                project__is_active=True
            ).order_by('-created_at')
        
        # Todas las actualizaciones recientes
        return ProjectUpdate.objects.filter(
            project__is_active=True
        ).select_related('project').order_by('-created_at')[:20]
    
    @action(detail=False, methods=['get'])
    def milestones(self, request):
        """Obtener solo los hitos importantes"""
        queryset = self.get_queryset().filter(is_milestone=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)