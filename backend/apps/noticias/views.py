from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import NewsPost
from .serializers import (
    NewsListSerializer,
    NewsDetailSerializer,
    NewsCreateUpdateSerializer
)


class NewsListView(generics.ListAPIView):
    """
    List all published news posts.
    Supports filtering by category and search.
    """
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'views']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = NewsPost.objects.filter(published=True).select_related('author')
        
        # Filter by category if provided
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter featured posts
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)
        
        return queryset


class NewsDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single news post by slug.
    Increments view count on each retrieval.
    """
    serializer_class = NewsDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return NewsPost.objects.filter(published=True).select_related('author')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NewsCreateView(generics.CreateAPIView):
    """
    Create a new news post (admin only).
    """
    serializer_class = NewsCreateUpdateSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsUpdateView(generics.UpdateAPIView):
    """
    Update an existing news post (admin only).
    """
    serializer_class = NewsCreateUpdateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return NewsPost.objects.all()


class NewsDeleteView(generics.DestroyAPIView):
    """
    Delete a news post (admin only).
    """
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return NewsPost.objects.all()


class NewsByDateView(generics.ListAPIView):
    """
    List news posts for a specific date.
    """
    serializer_class = NewsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        
        return NewsPost.objects.filter(
            published=True,
            created_at__year=year,
            created_at__month=month,
            created_at__day=day
        ).select_related('author').order_by('-created_at')