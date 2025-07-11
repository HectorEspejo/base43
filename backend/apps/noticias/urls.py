from django.urls import path
from .views import (
    NewsListView,
    NewsDetailView,
    NewsCreateView,
    NewsUpdateView,
    NewsDeleteView,
    NewsByDateView
)

app_name = 'noticias'

urlpatterns = [
    # List views
    path('', NewsListView.as_view(), name='news-list'),
    path('<int:year>/<int:month>/<int:day>/', NewsByDateView.as_view(), name='news-by-date'),
    
    # Detail view
    path('<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
    
    # CRUD operations (admin only)
    path('create/', NewsCreateView.as_view(), name='news-create'),
    path('<slug:slug>/update/', NewsUpdateView.as_view(), name='news-update'),
    path('<slug:slug>/delete/', NewsDeleteView.as_view(), name='news-delete'),
]