# -*- coding: utf-8 -*-
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that includes user data in response.
    Verifica que el usuario esté verificado antes de permitir el login.
    """
    def post(self, request, *args, **kwargs):
        # Primero verificar si el usuario existe y está verificado
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            if not user.is_verified:
                return Response({
                    'error': 'Su cuenta está pendiente de verificación. Por favor, espere a que un administrador verifique su cuenta.'
                }, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            pass  # Dejar que el TokenObtainPairView maneje el error
        
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            response.data['user'] = UserSerializer(user).data
        return response


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # No generar tokens para usuarios no verificados
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Cuenta creada exitosamente. Su cuenta está pendiente de verificación por un administrador.'
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserProfileSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change user password endpoint.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set new password
        user = self.get_object()
        user.set_password(serializer.data['new_password'])
        user.save()
        
        return Response({
            'message': 'Contraseña actualizada correctamente.'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout user by blacklisting the refresh token.
    """
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'message': 'Sesión cerrada correctamente.'
        }, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({
            'error': 'Token inválido.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user data.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class AvatarUploadView(generics.UpdateAPIView):
    """
    Upload user avatar.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            user.save()
            return Response({
                'message': 'Avatar actualizado correctamente.',
                'avatar': user.avatar.url if user.avatar else None
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'No se proporcionó ningún archivo.'
        }, status=status.HTTP_400_BAD_REQUEST)