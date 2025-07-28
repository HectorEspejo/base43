from rest_framework import serializers
from .models import Resource, ResourceCategory, ResourceImage, ResourceDocument


class ResourceCategorySerializer(serializers.ModelSerializer):
    """Serializer para las categorías de recursos"""
    resource_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ResourceCategory
        fields = ['id', 'name', 'description', 'icon', 'resource_count']
    
    def get_resource_count(self, obj):
        """Cuenta los recursos activos de esta categoría"""
        return obj.resource_set.filter(is_active=True).count()


class ResourceImageSerializer(serializers.ModelSerializer):
    """Serializer para las imágenes de recursos"""
    class Meta:
        model = ResourceImage
        fields = ['id', 'image', 'caption', 'is_main']


class ResourceDocumentSerializer(serializers.ModelSerializer):
    """Serializer para los documentos de recursos"""
    class Meta:
        model = ResourceDocument
        fields = ['id', 'title', 'file', 'description', 'created_at']


class ResourceListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados de recursos"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id', 'name', 'type', 'type_display', 'category', 'category_name',
            'address', 'city', 'phone', 'email',
            'latitude', 'longitude', 'is_featured'
        ]


class ResourceDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalles de recursos"""
    category = ResourceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ResourceCategory.objects.all(),
        source='category',
        write_only=True
    )
    images = ResourceImageSerializer(many=True, read_only=True)
    documents = ResourceDocumentSerializer(many=True, read_only=True)
    services_list = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id', 'name', 'type', 'type_display', 'category', 'category_id',
            'description', 'address', 'city', 'postal_code',
            'latitude', 'longitude', 'phone', 'email', 'website',
            'schedule', 'services', 'services_list', 'requirements',
            'is_active', 'is_featured', 'full_address',
            'images', 'documents', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """Asigna el usuario actual al crear un recurso"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ResourceCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear y actualizar recursos"""
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ResourceCategory.objects.all(),
        source='category'
    )
    
    class Meta:
        model = Resource
        fields = [
            'name', 'type', 'category_id', 'description',
            'address', 'city', 'postal_code', 'latitude', 'longitude',
            'phone', 'email', 'website', 'schedule', 'services',
            'requirements', 'is_active', 'is_featured'
        ]
    
    def validate_services(self, value):
        """Valida que los servicios estén separados por comas"""
        if value:
            # Limpia espacios extras
            services = [s.strip() for s in value.split(',') if s.strip()]
            return ', '.join(services)
        return value


class ResourceMapSerializer(serializers.ModelSerializer):
    """Serializer optimizado para vista de mapa"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id', 'name', 'type_display', 'category_name',
            'latitude', 'longitude', 'address', 'phone'
        ]