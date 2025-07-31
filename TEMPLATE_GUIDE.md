# Base43 Template Guide

Welcome to Base43! This guide will help you customize and extend this template for your specific project needs.

## 🚀 Getting Started

### 1. Initial Setup

After cloning/forking this repository:

1. **Search and Replace** - Replace all instances of "Base43" with your project name
2. **Update Branding** - Replace logo files and update color schemes
3. **Configure Environment** - Update `.env` files with your specific settings
4. **Clean Up** - Remove any modules you don't need

### 2. Project Structure Overview

```
base43/
├── backend/          # Django REST API
│   ├── apps/        # Modular Django applications
│   ├── core/        # Core settings and base classes
│   └── static/      # Static files
├── frontend/        # Vue.js SPA
│   ├── src/
│   │   ├── components/base/  # Reusable base components
│   │   ├── views/           # Page components
│   │   ├── stores/          # State management
│   │   └── services/        # API services
│   └── public/      # Static assets
└── docs/           # Documentation
```

## 🎨 Customization Guide

### Frontend Customization

#### 1. Theme and Branding

Edit `frontend/tailwind.config.js`:

```javascript
daisyui: {
  themes: [{
    yourtheme: {
      "primary": "#your-primary-color",
      "secondary": "#your-secondary-color",
      "accent": "#your-accent-color",
      // ... more colors
    }
  }]
}
```

Update `frontend/index.html`:
```html
<html lang="es" data-theme="yourtheme">
```

#### 2. Logo and Images

1. Add your logo as `frontend/public/logo.png`
2. Update favicon in `frontend/index.html`
3. Replace generic images in `frontend/public/`

#### 3. Using Base Components

The template includes reusable components in `frontend/src/components/base/`:

```vue
<template>
  <BaseCard title="My Card" :shadow="true" :hover="true">
    <p>Card content</p>
    <template #actions>
      <BaseButton @click="handleClick">Action</BaseButton>
    </template>
  </BaseCard>
</template>

<script setup>
import { BaseCard, BaseButton } from '@/components/base'
</script>
```

### Backend Customization

#### 1. Using Base Classes

Extend the provided base classes for consistent behavior:

```python
# models.py
from core.base_models import TimeStampedModel, PublishableModel

class Article(TimeStampedModel, PublishableModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    class Meta:
        ordering = ['-created_at']
```

```python
# views.py
from core.base_views import BaseModelViewSet

class ArticleViewSet(BaseModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    search_fields = ['title', 'content']
    filterset_fields = ['is_published']
```

```python
# serializers.py
from core.base_serializers import TimeStampedSerializer

class ArticleSerializer(TimeStampedSerializer):
    class Meta:
        model = Article
        fields = '__all__'
```

#### 2. Adding New Apps

1. Create new app:
```bash
cd backend
python manage.py startapp myapp
```

2. Add to `INSTALLED_APPS` in `backend/core/settings.py`

3. Create models extending base classes

4. Create API views and serializers

5. Add URLs to `backend/core/urls.py`

## 📦 Built-in Modules

### Available Modules

1. **Authentication** (`apps.authentication`)
   - User registration and login
   - JWT token management
   - Password reset

2. **Projects** (`apps.proyectos`)
   - Project showcase with categories
   - Image galleries
   - Project updates

3. **News/Blog** (`apps.noticias`)
   - Article management
   - Rich text editor
   - Categories and tags

4. **Chat** (`apps.chat`)
   - Real-time messaging
   - Chat rooms
   - WebSocket support

5. **Contact** (`apps.contacto`)
   - Contact forms
   - Email notifications
   - Admin management

6. **Partners** (`apps.partners`)
   - Team/partner profiles
   - Logo management

7. **Resources** (`apps.recursos`)
   - Resource directory
   - File management

8. **Repository** (`apps.repositorio`)
   - Document management
   - File uploads
   - Categorization

### Removing Modules

To remove unwanted modules:

1. Remove from `INSTALLED_APPS`
2. Delete the app directory
3. Remove URL includes from `urls.py`
4. Remove frontend views and routes
5. Run migrations to clean database

## 🔧 Common Customizations

### 1. Change API Prefix

In `backend/core/urls.py`, modify URL patterns:
```python
path('myapi/v1/auth/', include('apps.authentication.urls')),
```

Update frontend API service in `frontend/src/services/api.js`.

### 2. Add Custom Middleware

Create in `backend/core/middleware.py`:
```python
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        # Process response
        return response
```

Add to `MIDDLEWARE` in settings.

### 3. Customize Admin Panel

Edit `backend/static/admin/css/custom_admin.css` for styling.

### 4. Add New Frontend Route

In `frontend/src/router/index.js`:
```javascript
{
  path: '/my-page',
  name: 'MyPage',
  component: () => import('@/views/MyPage.vue')
}
```

### 5. Environment-Specific Settings

Create environment-specific settings:
- `backend/core/settings_dev.py`
- `backend/core/settings_prod.py`

## 🏗️ Building for Production

### Backend

1. Update `settings.py`:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Set up proper database
   - Configure email settings

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Run with Gunicorn:
```bash
gunicorn core.wsgi:application
```

### Frontend

1. Create production env:
```bash
echo "VITE_API_URL=https://api.yourdomain.com" > .env.production
```

2. Build:
```bash
npm run build
```

3. Deploy `dist/` folder with nginx or similar.

## 📚 Best Practices

1. **Keep it Modular** - Each app should be self-contained
2. **Use Base Classes** - Leverage provided base classes for consistency
3. **Follow Conventions** - Maintain the established patterns
4. **Document Changes** - Update docs as you customize
5. **Test Everything** - Add tests for new functionality

## 🤝 Contributing Back

If you create useful generic features, consider contributing back to Base43:

1. Keep features generic and reusable
2. Follow existing code style
3. Add documentation
4. Include tests
5. Submit a pull request

## 📞 Support

- Documentation: Check the `docs/` directory
- Issues: Use GitHub issues for bugs/features
- Community: Join our discussions

---

Happy coding with Base43! 🚀