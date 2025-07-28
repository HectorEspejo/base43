from rest_framework import serializers
from .models import ProjectCategory, Project, ProjectImage, ProjectDocument, ProjectUpdate


class ProjectCategorySerializer(serializers.ModelSerializer):
    """Serializer para las categorías de proyectos"""
    projects_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ProjectCategory
        fields = [
            'id', 'name', 'slug', 'description', 'icon',
            'order', 'is_active', 'projects_count'
        ]


class ProjectImageSerializer(serializers.ModelSerializer):
    """Serializer para las imágenes del proyecto"""
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'order']


class ProjectDocumentSerializer(serializers.ModelSerializer):
    """Serializer para los documentos del proyecto"""
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectDocument
        fields = [
            'id', 'title', 'file', 'description', 
            'is_public', 'file_size', 'created_at'
        ]
    
    def get_file_size(self, obj):
        """Devuelve el tamaño del archivo en formato legible"""
        if obj.file:
            size = obj.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
        return None


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """Serializer para las actualizaciones del proyecto"""
    created_by_name = serializers.CharField(
        source='created_by.get_full_name',
        read_only=True
    )
    
    class Meta:
        model = ProjectUpdate
        fields = [
            'id', 'title', 'content', 'image', 'is_milestone',
            'created_by_name', 'created_at', 'updated_at'
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer para listado de proyectos (versión reducida)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    location = serializers.CharField(source='get_location', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'category', 'category_name',
            'city', 'province', 'location', 'short_description',
            'units', 'participants', 'status', 'status_display',
            'image', 'is_featured'
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalles de proyectos"""
    category = ProjectCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all(),
        source='category',
        write_only=True
    )
    images = ProjectImageSerializer(many=True, read_only=True)
    documents = serializers.SerializerMethodField()
    updates = serializers.SerializerMethodField()
    location = serializers.CharField(source='get_location', read_only=True)
    features_list = serializers.ListField(
        source='get_features_list',
        read_only=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_class = serializers.CharField(source='get_status_display_class', read_only=True)
    partner_name = serializers.CharField(source='partner.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'category', 'category_id',
            'city', 'province', 'address', 'coordinates', 'location',
            'short_description', 'description', 'units', 'participants',
            'status', 'status_display', 'status_class', 'start_date',
            'estimated_completion', 'features', 'features_list',
            'investment_range', 'financing_type', 'partner_name',
            'image', 'images', 'documents', 'updates', 'is_featured',
            'is_active', 'views', 'website', 'video_url',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'views', 'created_at', 'updated_at']
    
    def get_documents(self, obj):
        """Filtrar documentos según el usuario"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            documents = obj.documents.all()
        else:
            documents = obj.documents.filter(is_public=True)
        return ProjectDocumentSerializer(documents, many=True).data
    
    def get_updates(self, obj):
        """Obtener las últimas actualizaciones"""
        updates = obj.updates.all().order_by('-created_at')[:5]  # Últimas 5 actualizaciones
        return ProjectUpdateSerializer(updates, many=True).data
    
    def validate(self, data):
        """Validaciones personalizadas"""
        # Validar fechas
        start_date = data.get('start_date')
        estimated_completion = data.get('estimated_completion')
        
        if start_date and estimated_completion:
            if estimated_completion < start_date:
                raise serializers.ValidationError({
                    'estimated_completion': 'La fecha de finalización debe ser posterior a la fecha de inicio'
                })
        
        # Validar participantes vs unidades
        participants = data.get('participants', 0)
        units = data.get('units', 1)
        
        if participants > units * 5:  # Máximo 5 participantes por unidad
            raise serializers.ValidationError({
                'participants': 'El número de participantes parece excesivo para las unidades disponibles'
            })
        
        return data


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar proyectos"""
    class Meta:
        model = Project
        exclude = ['slug', 'views', 'created_by']
    
    def validate_name(self, value):
        """Validar que el nombre sea único"""
        instance = self.instance
        if Project.objects.exclude(pk=instance.pk if instance else None).filter(name__iexact=value).exists():
            raise serializers.ValidationError('Ya existe un proyecto con este nombre')
        return value