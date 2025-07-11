from rest_framework import serializers
import os
from .models import Category, Directory, RepositoryFile
from apps.authentication.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for repository categories."""
    directories_count = serializers.IntegerField(read_only=True)
    files_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 
            'order', 'is_active', 'directories_count', 'files_count'
        ]


class RepositoryFileSerializer(serializers.ModelSerializer):
    """Serializer for repository files."""
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    license_display = serializers.CharField(source='get_license_display', read_only=True)
    extension = serializers.CharField(source='get_extension', read_only=True)
    icon = serializers.CharField(source='get_icon', read_only=True)
    can_preview = serializers.SerializerMethodField()
    size_display = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    download_name = serializers.SerializerMethodField()
    
    class Meta:
        model = RepositoryFile
        fields = [
            'id', 'name', 'description', 'license', 'license_display',
            'size', 'size_display', 'mime_type', 'extension', 'icon',
            'uploaded_by', 'uploaded_by_name', 'uploaded_at', 'modified_at',
            'downloads', 'is_public', 'is_hidden', 'can_preview', 'file_url',
            'download_name'
        ]
    
    def get_size_display(self, obj):
        if not obj.size:
            return "N/A"
        size = obj.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_can_preview(self, obj):
        return obj.can_preview()
    
    def get_download_name(self, obj):
        """Get the proper download name with extension."""
        if obj.file:
            # If name doesn't have extension, use the original filename
            if not os.path.splitext(obj.name)[1]:
                return os.path.basename(obj.file.name)
            else:
                return obj.name
        return obj.name


class DirectorySerializer(serializers.ModelSerializer):
    """Serializer for directories."""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    files_count = serializers.IntegerField(read_only=True)
    subdirectories_count = serializers.IntegerField(read_only=True)
    full_path = serializers.CharField(source='get_full_path', read_only=True)
    
    class Meta:
        model = Directory
        fields = [
            'id', 'name', 'category', 'parent', 'created_by', 'created_by_name',
            'created_at', 'is_public', 'files_count', 'subdirectories_count', 'full_path'
        ]


class DirectoryDetailSerializer(DirectorySerializer):
    """Detailed serializer for directory with subdirectories and files."""
    subdirectories = serializers.SerializerMethodField()
    files = RepositoryFileSerializer(many=True, read_only=True)
    
    class Meta(DirectorySerializer.Meta):
        fields = DirectorySerializer.Meta.fields + ['subdirectories', 'files']
    
    def get_subdirectories(self, obj):
        from django.db.models import Count
        subdirs = obj.subdirectories.annotate(
            files_count=Count('files'),
            subdirectories_count=Count('subdirectories')
        )
        return DirectorySerializer(subdirs, many=True, context=self.context).data


class CategoryDetailSerializer(CategorySerializer):
    """Detailed serializer for category with root directories and files."""
    root_directories = serializers.SerializerMethodField()
    root_files = serializers.SerializerMethodField()
    
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['root_directories', 'root_files']
    
    def get_root_directories(self, obj):
        # Get only root directories (without parent)
        from django.db.models import Count
        directories = obj.directories.filter(parent=None).annotate(
            files_count=Count('files'),
            subdirectories_count=Count('subdirectories')
        )
        return DirectorySerializer(directories, many=True, context=self.context).data
    
    def get_root_files(self, obj):
        # Get only files without directory (root files)
        files = obj.files.filter(directory=None)
        # Filter based on permissions
        request = self.context.get('request')
        if request and request.user:
            filtered_files = []
            for file in files:
                if file.check_permission(request.user):
                    filtered_files.append(file)
            return RepositoryFileSerializer(filtered_files, many=True, context=self.context).data
        return []


class FileUploadSerializer(serializers.ModelSerializer):
    """Serializer for file uploads."""
    
    class Meta:
        model = RepositoryFile
        fields = [
            'name', 'file', 'category', 'directory', 'description',
            'license', 'is_public', 'is_hidden', 'allowed_users'
        ]
    
    def validate_file(self, value):
        # Additional file validation can be added here
        return value


class BreadcrumbSerializer(serializers.Serializer):
    """Serializer for breadcrumb navigation."""
    name = serializers.CharField()
    path = serializers.CharField()
    type = serializers.CharField()  # 'category' or 'directory'
    id = serializers.IntegerField()