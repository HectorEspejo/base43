from django.urls import path
from . import views

app_name = 'repositorio'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Directories
    path('directories/<int:pk>/', views.DirectoryDetailView.as_view(), name='directory-detail'),
    path('directories/<int:pk>/download/', views.DirectoryDownloadView.as_view(), name='directory-download'),
    
    # Files
    path('files/', views.FileListView.as_view(), name='file-list'),
    path('files/<int:pk>/', views.FileDetailView.as_view(), name='file-detail'),
    path('files/<int:pk>/download/', views.FileDownloadView.as_view(), name='file-download'),
    path('files/<int:pk>/preview/', views.FilePreviewView.as_view(), name='file-preview'),
    
    # Upload
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    
    # Utils
    path('breadcrumb/', views.get_breadcrumb, name='breadcrumb'),
    path('stats/', views.repository_stats, name='stats'),
]