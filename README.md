# Base43 - Modern Web Application Template

![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3.3-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Node](https://img.shields.io/badge/Node.js-18+-orange.svg)

Base43 is a modern, full-stack web application template designed to jumpstart your web projects. Built with Django REST Framework and Vue.js 3, it provides a solid foundation with essential features already implemented.

## 🚀 Features

### Backend (Django)
- **RESTful API** with Django REST Framework
- **JWT Authentication** with token refresh
- **User Management** with profiles and permissions
- **WebSocket Support** via Django Channels
- **PostgreSQL** for relational data
- **Redis** for caching and real-time features
- **Celery** for async task processing
- **API Documentation** with Swagger/ReDoc
- **Admin Panel** with custom styling

### Frontend (Vue.js 3)
- **Modern UI** with Tailwind CSS and DaisyUI
- **State Management** with Pinia
- **Vue Router** for SPA navigation
- **Real-time Chat** with Socket.io
- **Responsive Design** mobile-first approach
- **Form Validation** and error handling
- **Dark Mode** support

### Built-in Modules
- **Authentication System** (login, register, password reset)
- **User Profiles** with customizable fields
- **News/Blog System** with rich text editor
- **Project Showcase** with categories and filters
- **Document Repository** with file management
- **Contact Forms** with email notifications
- **Partner/Team Management**
- **Resource Directory**
- **Real-time Chat** with rooms

## 📋 Requirements

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

## 🛠️ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/base43.git
cd base43
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Configure environment
echo "VITE_API_URL=http://localhost:8000" > .env.development

# Run development server
npm run dev
```

### 4. Additional Services

For full functionality, run Redis:
```bash
redis-server
```

For async tasks, run Celery:
```bash
cd backend
celery -A core worker -l info
```

## 🏗️ Project Structure

```
base43/
├── backend/
│   ├── apps/           # Django applications
│   │   ├── authentication/
│   │   ├── chat/
│   │   ├── contacto/
│   │   ├── noticias/
│   │   ├── oferta/
│   │   ├── partners/
│   │   ├── proyectos/
│   │   ├── recursos/
│   │   └── repositorio/
│   ├── core/           # Django settings
│   ├── static/         # Static files
│   ├── media/          # User uploads
│   └── requirements.txt
├── frontend/
│   ├── public/         # Static assets
│   ├── src/
│   │   ├── components/ # Vue components
│   │   ├── views/      # Page components
│   │   ├── stores/     # Pinia stores
│   │   ├── services/   # API services
│   │   └── router/     # Vue Router config
│   ├── package.json
│   └── vite.config.js
└── docs/               # Documentation
```

## 🔧 Configuration

### Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend (.env)**
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=base43_db
POSTGRES_USER=base43_user
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Frontend (.env.development)**
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 📚 Available APIs

- `/api/v1/auth/` - Authentication endpoints
- `/api/v1/proyectos/` - Projects management
- `/api/v1/noticias/` - News/Blog posts
- `/api/v1/oferta/` - Services catalog
- `/api/v1/repositorio/` - Document repository
- `/api/v1/chat/` - Chat functionality
- `/api/v1/contacto/` - Contact forms
- `/api/v1/partners/` - Partners management
- `/api/v1/recursos/` - Resources directory

API documentation available at:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## 🎨 Customization

### Theming
Edit `frontend/tailwind.config.js` to customize colors and theme:

```javascript
daisyui: {
  themes: [{
    base43: {
      "primary": "#22c55e",
      "secondary": "#fbbc04",
      // ... customize your theme
    }
  }]
}
```

### Adding New Modules
1. Create Django app: `python manage.py startapp app_name`
2. Add to `INSTALLED_APPS` in settings
3. Create models, serializers, views, and URLs
4. Create corresponding Vue components
5. Add routes to frontend router

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📦 Production Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed production deployment instructions.

### Quick Production Build

**Backend:**
```bash
python manage.py collectstatic --noinput
gunicorn core.wsgi:application
```

**Frontend:**
```bash
npm run build
# Serve dist/ folder with nginx
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Django and Vue.js
- UI components from DaisyUI
- Icons from Heroicons

## 💬 Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/your-org/base43/issues)
- Email: support@base43.org

---

**Base43** - Your foundation for modern web applications 🚀