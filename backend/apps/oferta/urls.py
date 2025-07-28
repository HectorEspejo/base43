from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceCategoryViewSet, ServiceViewSet, ServiceInquiryViewSet

app_name = 'oferta'

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet, basename='service-category')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'inquiries', ServiceInquiryViewSet, basename='service-inquiry')

urlpatterns = [
    path('', include(router.urls)),
]