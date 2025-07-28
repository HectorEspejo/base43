from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectCategoryViewSet,
    ProjectViewSet,
    ProjectImageViewSet,
    ProjectUpdateViewSet
)

app_name = 'proyectos'

router = DefaultRouter()
router.register(r'categories', ProjectCategoryViewSet, basename='project-category')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'updates', ProjectUpdateViewSet, basename='project-update')

# Nested routes for project images
project_router = DefaultRouter()
project_router.register(r'images', ProjectImageViewSet, basename='project-images')

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<slug:project_slug>/', include(project_router.urls)),
]