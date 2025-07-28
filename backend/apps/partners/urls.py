from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartnerCategoryViewSet, PartnerViewSet, PartnerTestimonialViewSet

router = DefaultRouter()
router.register(r'categories', PartnerCategoryViewSet, basename='partner-category')
router.register(r'partners', PartnerViewSet, basename='partner')
router.register(r'testimonials', PartnerTestimonialViewSet, basename='partner-testimonial')

app_name = 'partners'

urlpatterns = [
    path('', include(router.urls)),
]