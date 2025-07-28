from rest_framework import serializers
from .models import ServiceCategory, Service, ServiceInquiry


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer para las categorías de servicios"""
    services_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ServiceCategory
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'color',
            'order', 'is_active', 'services_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']


class ServiceListSerializer(serializers.ModelSerializer):
    """Serializer para listado de servicios (versión reducida)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    price_display = serializers.CharField(source='get_price_display', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'category', 'category_name',
            'short_description', 'price_type', 'price_display',
            'is_featured', 'is_active', 'image'
        ]


class ServiceDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalles de servicios"""
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True
    )
    features_list = serializers.ListField(
        source='get_features_list',
        read_only=True
    )
    price_display = serializers.CharField(source='get_price_display', read_only=True)
    inquiries_count = serializers.IntegerField(
        source='inquiries.count',
        read_only=True
    )
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'category', 'category_id',
            'description', 'short_description', 'features', 'features_list',
            'requirements', 'duration', 'price_type', 'price_min', 'price_max',
            'price_note', 'price_display', 'provider_name', 'provider_email',
            'provider_phone', 'provider_website', 'image', 'is_featured',
            'is_active', 'order', 'views', 'inquiries_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'views', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validación personalizada para los precios"""
        price_type = data.get('price_type', self.instance.price_type if self.instance else None)
        price_min = data.get('price_min')
        price_max = data.get('price_max')
        
        if price_type in ['fixed', 'hourly', 'project']:
            if price_min and price_max and price_min > price_max:
                raise serializers.ValidationError({
                    'price_max': 'El precio máximo debe ser mayor que el precio mínimo'
                })
        
        return data


class ServiceInquirySerializer(serializers.ModelSerializer):
    """Serializer para consultas de servicios"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = ServiceInquiry
        fields = [
            'id', 'service', 'service_name', 'name', 'email',
            'phone', 'message', 'is_read', 'is_answered',
            'notes', 'created_at', 'answered_at'
        ]
        read_only_fields = [
            'is_read', 'is_answered', 'notes', 
            'created_at', 'answered_at', 'answered_by'
        ]


class ServiceInquiryAdminSerializer(serializers.ModelSerializer):
    """Serializer para administración de consultas"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    answered_by_username = serializers.CharField(
        source='answered_by.username',
        read_only=True
    )
    
    class Meta:
        model = ServiceInquiry
        fields = '__all__'
        read_only_fields = ['created_at']