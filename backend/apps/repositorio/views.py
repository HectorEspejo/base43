from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from django.db.models import Count, Q, Sum
from django.db import models
import os
import zipfile
import tempfile
from io import BytesIO

from .models import Category, Directory, RepositoryFile
from .serializers import (
    CategorySerializer,
    CategoryDetailSerializer,
    DirectorySerializer,
    DirectoryDetailSerializer,
    RepositoryFileSerializer,
    FileUploadSerializer,
    BreadcrumbSerializer
)


class RepositoryPermission(permissions.BasePermission):
    """Custom permission for repository access."""
    
    def has_object_permission(self, request, view, obj):
        # Check file permissions
        if isinstance(obj, RepositoryFile):
            return obj.check_permission(request.user)
        
        # Check directory permissions
        if isinstance(obj, Directory):
            if not obj.is_public and not request.user.is_authenticated:
                return False
            if obj.allowed_users.exists():
                return obj.allowed_users.filter(id=request.user.id).exists()
        
        return True


class CategoryListView(generics.ListAPIView):
    """List all active categories."""
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).annotate(
            directories_count=Count('directories'),
            files_count=Count('files')
        ).order_by('order', 'name')


class CategoryDetailView(generics.RetrieveAPIView):
    """Get category details with root directories and files."""
    serializer_class = CategoryDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related(
            'directories__subdirectories',
            'files'
        )


class DirectoryDetailView(generics.RetrieveAPIView):
    """Get directory details with subdirectories and files."""
    serializer_class = DirectoryDetailSerializer
    permission_classes = [RepositoryPermission]
    
    def get_queryset(self):
        return Directory.objects.all().annotate(
            files_count=Count('files'),
            subdirectories_count=Count('subdirectories')
        ).prefetch_related('subdirectories', 'files')


class FileListView(generics.ListAPIView):
    """List files with filtering options."""
    serializer_class = RepositoryFileSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = RepositoryFile.objects.filter(is_hidden=False)
        
        # Filter by category
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by directory
        directory_id = self.request.query_params.get('directory')
        if directory_id:
            queryset = queryset.filter(directory_id=directory_id)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Filter by license
        license = self.request.query_params.get('license')
        if license:
            queryset = queryset.filter(license=license)
        
        # Filter based on user permissions
        filtered_files = []
        for file in queryset:
            if file.check_permission(self.request.user):
                filtered_files.append(file.id)
        
        return queryset.filter(id__in=filtered_files).select_related(
            'category', 'directory', 'uploaded_by'
        ).order_by('-uploaded_at')


class FileDetailView(generics.RetrieveAPIView):
    """Get file details."""
    serializer_class = RepositoryFileSerializer
    permission_classes = [RepositoryPermission]
    
    def get_queryset(self):
        return RepositoryFile.objects.all()


class FileDownloadView(APIView):
    """Download a file."""
    permission_classes = [RepositoryPermission]
    
    def get(self, request, pk):
        file_obj = get_object_or_404(RepositoryFile, pk=pk)
        
        # Check permissions
        self.check_object_permissions(request, file_obj)
        
        # Increment download counter
        file_obj.increment_downloads()
        
        # Serve file
        # Get the original filename with extension
        original_filename = os.path.basename(file_obj.file.name)
        # If the stored name doesn't have extension, use the original filename
        if not os.path.splitext(file_obj.name)[1]:
            download_name = original_filename
        else:
            download_name = file_obj.name
            
        response = FileResponse(
            file_obj.file.open('rb'),
            as_attachment=True,
            filename=download_name
        )
        response['Content-Type'] = file_obj.mime_type or 'application/octet-stream'
        return response


class FilePreviewView(APIView):
    """Preview a file (for supported formats)."""
    permission_classes = [RepositoryPermission]
    
    def get(self, request, pk):
        file_obj = get_object_or_404(RepositoryFile, pk=pk)
        
        # Check permissions
        self.check_object_permissions(request, file_obj)
        
        if not file_obj.can_preview():
            return Response(
                {'error': 'Este archivo no soporta vista previa'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # For PDFs and images, return the file directly
        ext = file_obj.get_extension().lower()
        if ext in ['pdf', 'jpg', 'jpeg', 'png', 'gif', 'svg']:
            response = FileResponse(
                file_obj.file.open('rb'),
                content_type=file_obj.mime_type
            )
            response['Content-Disposition'] = f'inline; filename="{file_obj.name}"'
            return response
        
        # For text files, return content
        if ext in ['txt', 'md']:
            content = file_obj.file.read().decode('utf-8', errors='ignore')
            return Response({'content': content, 'type': 'text'})
        
        return Response({'error': 'Formato no soportado'}, status=status.HTTP_400_BAD_REQUEST)


class DirectoryDownloadView(APIView):
    """Download directory as ZIP file."""
    permission_classes = [RepositoryPermission]
    
    def get(self, request, pk):
        directory = get_object_or_404(Directory, pk=pk)
        
        # Check permissions
        self.check_object_permissions(request, directory)
        
        # Create ZIP file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add all files from this directory and subdirectories
            self._add_directory_to_zip(zip_file, directory, directory.name)
        
        # Prepare response
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{directory.name}.zip"'
        
        return response
    
    def _add_directory_to_zip(self, zip_file, directory, path):
        """Recursively add directory contents to ZIP."""
        # Add files in current directory
        for file in directory.files.filter(is_hidden=False):
            if file.check_permission(self.request.user):
                # Get the proper filename with extension
                if not os.path.splitext(file.name)[1] and file.file:
                    # If name doesn't have extension, use the original filename
                    filename = os.path.basename(file.file.name)
                else:
                    filename = file.name
                
                file_path = os.path.join(path, filename)
                zip_file.writestr(file_path, file.file.read())
        
        # Add subdirectories
        for subdir in directory.subdirectories.all():
            subdir_path = os.path.join(path, subdir.name)
            self._add_directory_to_zip(zip_file, subdir, subdir_path)


class FileUploadView(generics.CreateAPIView):
    """Upload a new file (admin only)."""
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_breadcrumb(request):
    """Get breadcrumb navigation data."""
    path_type = request.GET.get('type')  # 'category' or 'directory'
    path_id = request.GET.get('id')
    
    breadcrumb = []
    
    if path_type == 'category' and path_id:
        category = get_object_or_404(Category, pk=path_id)
        breadcrumb.append({
            'name': category.name,
            'path': category.slug,
            'type': 'category',
            'id': category.id
        })
    
    elif path_type == 'directory' and path_id:
        directory = get_object_or_404(Directory, pk=path_id)
        
        # Build breadcrumb from category to current directory
        breadcrumb.append({
            'name': directory.category.name,
            'path': directory.category.slug,
            'type': 'category',
            'id': directory.category.id
        })
        
        # Add parent directories
        parents = []
        current = directory
        while current.parent:
            parents.insert(0, current.parent)
            current = current.parent
        
        for parent in parents:
            breadcrumb.append({
                'name': parent.name,
                'path': str(parent.id),
                'type': 'directory',
                'id': parent.id
            })
        
        # Add current directory
        breadcrumb.append({
            'name': directory.name,
            'path': str(directory.id),
            'type': 'directory',
            'id': directory.id
        })
    
    serializer = BreadcrumbSerializer(breadcrumb, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def repository_stats(request):
    """Get repository statistics."""
    stats = {
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_directories': Directory.objects.count(),
        'total_files': RepositoryFile.objects.filter(is_hidden=False).count(),
        'total_downloads': RepositoryFile.objects.aggregate(
            total=models.Sum('downloads')
        )['total'] or 0,
        'licenses': list(
            RepositoryFile.objects.filter(is_hidden=False)
            .values('license')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
    }
    return Response(stats)