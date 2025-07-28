from rest_framework import serializers
from .models import PartnerCategory, Partner, PartnerTestimonial, PartnerProject


class PartnerCategorySerializer(serializers.ModelSerializer):
    """Serializer para las categorías de partners"""
    partners_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = PartnerCategory
        fields = [
            'id', 'name', 'slug', 'description', 
            'order', 'is_active', 'partners_count'
        ]


class PartnerTestimonialSerializer(serializers.ModelSerializer):
    """Serializer para los testimonios de partners"""
    partner_name = serializers.CharField(source='partner.name', read_only=True)
    
    class Meta:
        model = PartnerTestimonial
        fields = [
            'id', 'partner', 'partner_name', 'author', 
            'role', 'content', 'is_active', 'created_at'
        ]


class PartnerProjectSerializer(serializers.ModelSerializer):
    """Serializer para los proyectos de partners"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_slug = serializers.CharField(source='project.slug', read_only=True)
    partner_name = serializers.CharField(source='partner.name', read_only=True)
    
    class Meta:
        model = PartnerProject
        fields = [
            'id', 'partner', 'partner_name', 'project', 'project_name',
            'project_slug', 'role', 'description', 'start_date', 
            'end_date', 'is_active'
        ]


class PartnerListSerializer(serializers.ModelSerializer):
    """Serializer para listado de partners (versión reducida)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    location = serializers.CharField(source='get_location', read_only=True)
    partner_type_display = serializers.CharField(source='get_partner_type_display', read_only=True)
    
    class Meta:
        model = Partner
        fields = [
            'id', 'name', 'slug', 'partner_type', 'partner_type_display',
            'category', 'category_name', 'city', 'province', 'location',
            'logo', 'is_featured', 'is_active'
        ]


class PartnerDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalles de partners"""
    category = PartnerCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=PartnerCategory.objects.all(),
        source='category',
        write_only=True
    )
    testimonials = PartnerTestimonialSerializer(many=True, read_only=True)
    partner_projects = PartnerProjectSerializer(many=True, read_only=True)
    location = serializers.CharField(source='get_location', read_only=True)
    partner_type_display = serializers.CharField(source='get_partner_type_display', read_only=True)
    collaboration_areas_list = serializers.ListField(
        source='get_collaboration_areas_list',
        read_only=True
    )
    social_media_links = serializers.DictField(
        source='get_social_media_links',
        read_only=True
    )
    
    class Meta:
        model = Partner
        fields = [
            'id', 'name', 'slug', 'partner_type', 'partner_type_display',
            'category', 'category_id', 'description', 'mission',
            'contact_person', 'email', 'phone', 'website',
            'address', 'city', 'province', 'postal_code', 'location',
            'linkedin', 'twitter', 'facebook', 'instagram',
            'social_media_links', 'collaboration_areas', 'collaboration_areas_list',
            'collaboration_start', 'logo', 'featured_image',
            'is_featured', 'is_active', 'order', 'testimonials',
            'partner_projects', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validar que el nombre sea único"""
        instance = self.instance
        if Partner.objects.exclude(pk=instance.pk if instance else None).filter(name__iexact=value).exists():
            raise serializers.ValidationError('Ya existe un partner con este nombre')
        return value


class PartnerCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar partners"""
    class Meta:
        model = Partner
        exclude = ['slug']
    
    def validate_name(self, value):
        """Validar que el nombre sea único"""
        instance = self.instance
        if Partner.objects.exclude(pk=instance.pk if instance else None).filter(name__iexact=value).exists():
            raise serializers.ValidationError('Ya existe un partner con este nombre')
        return value