"""
Base serializers for Base43 project.
Provides common serializers and mixins for API serialization.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class TimeStampedSerializer(serializers.ModelSerializer):
    """
    Base serializer that includes timestamp fields.
    """
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        abstract = True


class AuthorSerializer(TimeStampedSerializer):
    """
    Base serializer that includes author tracking fields.
    """
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    updated_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()
    
    class Meta:
        abstract = True
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None
    
    def get_updated_by_name(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return None


class UserSerializer(serializers.ModelSerializer):
    """
    Base serializer for User model with commonly needed fields.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class WritableNestedSerializer(serializers.ModelSerializer):
    """
    Base serializer that handles writable nested relationships.
    """
    
    def create(self, validated_data):
        """
        Create instance with nested relationships.
        """
        nested_data = self._pop_nested_data(validated_data)
        instance = super().create(validated_data)
        self._create_nested_objects(instance, nested_data)
        return instance
    
    def update(self, instance, validated_data):
        """
        Update instance with nested relationships.
        """
        nested_data = self._pop_nested_data(validated_data)
        instance = super().update(instance, validated_data)
        self._update_nested_objects(instance, nested_data)
        return instance
    
    def _pop_nested_data(self, validated_data):
        """
        Extract nested data from validated_data.
        Override this method in subclasses.
        """
        return {}
    
    def _create_nested_objects(self, instance, nested_data):
        """
        Create nested objects.
        Override this method in subclasses.
        """
        pass
    
    def _update_nested_objects(self, instance, nested_data):
        """
        Update nested objects.
        Override this method in subclasses.
        """
        pass


class DynamicFieldsSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    
    Usage:
        serializer = MySerializer(queryset, fields=['id', 'name'])
    """
    
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        
        if exclude_fields is not None:
            # Remove fields specified in `exclude_fields` argument
            for field_name in exclude_fields:
                self.fields.pop(field_name, None)


class BulkSerializerMixin:
    """
    Mixin to add bulk operations support to serializers.
    """
    
    def create(self, validated_data):
        """
        Override create to handle bulk creation if list is provided.
        """
        if isinstance(validated_data, list):
            return self.create_bulk(validated_data)
        return super().create(validated_data)
    
    def create_bulk(self, validated_data_list):
        """
        Create multiple instances at once.
        """
        model_class = self.Meta.model
        created_objects = []
        
        for validated_data in validated_data_list:
            obj = model_class(**validated_data)
            created_objects.append(obj)
        
        model_class.objects.bulk_create(created_objects)
        return created_objects


class FileUploadSerializer(serializers.Serializer):
    """
    Base serializer for file upload handling.
    """
    file = serializers.FileField()
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)
    
    def validate_file(self, value):
        """
        Validate file size and type.
        Override this method to add custom validation.
        """
        # Check file size (default max 10MB)
        max_size = getattr(self, 'max_file_size', 10 * 1024 * 1024)
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size cannot exceed {max_size / 1024 / 1024}MB"
            )
        
        return value


class ImageUploadSerializer(FileUploadSerializer):
    """
    Serializer specifically for image uploads with validation.
    """
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    max_file_size = 5 * 1024 * 1024  # 5MB
    
    def validate_file(self, value):
        value = super().validate_file(value)
        
        # Check file extension
        ext = value.name.split('.')[-1].lower()
        if ext not in self.allowed_extensions:
            raise serializers.ValidationError(
                f"Invalid file type. Allowed types: {', '.join(self.allowed_extensions)}"
            )
        
        return value


class PaginatedListSerializer(serializers.Serializer):
    """
    Base serializer for paginated responses.
    """
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()


class ErrorResponseSerializer(serializers.Serializer):
    """
    Standard error response serializer.
    """
    success = serializers.BooleanField(default=False)
    message = serializers.CharField()
    errors = serializers.DictField(required=False)
    code = serializers.CharField(required=False)


class SuccessResponseSerializer(serializers.Serializer):
    """
    Standard success response serializer.
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    data = serializers.DictField(required=False)


# Validation mixins
class PhoneNumberValidationMixin:
    """
    Mixin to add phone number validation.
    """
    
    def validate_phone(self, value):
        """
        Validate phone number format.
        """
        import re
        
        # Remove all non-digit characters
        cleaned = re.sub(r'\D', '', value)
        
        # Check length (adjust based on your requirements)
        if len(cleaned) < 9 or len(cleaned) > 15:
            raise serializers.ValidationError(
                "Invalid phone number format"
            )
        
        return cleaned


class EmailValidationMixin:
    """
    Mixin to add enhanced email validation.
    """
    
    def validate_email(self, value):
        """
        Enhanced email validation.
        """
        value = value.lower().strip()
        
        # Check if email already exists (if creating new record)
        if self.instance is None:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    "A user with this email already exists"
                )
        
        return value