# Calicanto - Plataforma Comunitaria de Vivienda

## 📋 Descripción

Calicanto es una plataforma web comunitaria diseñada para conectar personas, proyectos y recursos en el ámbito de la vivienda colaborativa y sostenible. La plataforma facilita la creación de comunidades, el intercambio de conocimientos y la gestión de proyectos de vivienda alternativos.

## 🚀 Características Principales

- **Catálogo de Servicios (OFERTA)**: Directorio de profesionales y servicios especializados
- **Repositorio de Documentos**: Gestión de documentación con licencias Copyleft
- **Showcase de Proyectos**: Visualización de proyectos de vivienda comunitaria
- **Feed de Noticias**: Actualizaciones y novedades de la comunidad
- **Chat en Tiempo Real**: Comunicación instantánea entre miembros
- **Directorio de Partners**: Red de organizaciones colaboradoras
- **Sistema de Contacto**: Formularios y gestión de comunicaciones

## 🛠️ Stack Tecnológico

### Backend
- Django 4.2 + Django REST Framework
- PostgreSQL (datos relacionales)
- MongoDB (documentos)
- Redis (cache y mensajería)
- Celery (tareas asíncronas)
- Django Channels (WebSockets)

### Frontend
- Vue.js 3 (Composition API)
- Vite (build tool)
- Tailwind CSS + DaisyUI
- Pinia (gestión de estado)
- Socket.io-client (chat en tiempo real)

### DevOps
- Docker + Docker Compose
- Nginx (servidor web)
- Gunicorn (servidor WSGI)

## 📦 Instalación y Configuración

### Prerrequisitos
- Docker y Docker Compose instalados
- Git

### Instalación Rápida con Docker

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/calicanto.git
cd calicanto/web
```

2. Copia el archivo de configuración de ejemplo:
```bash
cp backend/.env.example backend/.env
```

3. Edita el archivo `.env` con tus configuraciones

4. Inicia los servicios con Docker:
```bash
cd docker
docker-compose up -d
```

5. Ejecuta las migraciones:
```bash
docker-compose exec backend python manage.py migrate
```

6. Crea un superusuario:
```bash
docker-compose exec backend python manage.py createsuperuser
```

7. Accede a la aplicación:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Admin Django: http://localhost:8000/admin/

### Instalación Manual (Desarrollo)

#### Backend

1. Crea un entorno virtual:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

4. Ejecuta las migraciones:
```bash
python manage.py migrate
```

5. Inicia el servidor de desarrollo:
```bash
python manage.py runserver
```

#### Frontend

1. Instala las dependencias:
```bash
cd frontend
npm install
```

2. Inicia el servidor de desarrollo:
```bash
npm run dev
```

## 🏗️ Estructura del Proyecto

```
web/
├── backend/
│   ├── core/              # Configuración principal Django
│   ├── apps/              # Aplicaciones Django
│   │   ├── authentication/
│   │   ├── oferta/
│   │   ├── repositorio/
│   │   ├── proyectos/
│   │   ├── noticias/
│   │   ├── chat/
│   │   ├── partners/
│   │   └── contacto/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # Componentes Vue reutilizables
│   │   ├── views/         # Vistas/páginas
│   │   ├── stores/        # Stores de Pinia
│   │   ├── services/      # Servicios API
│   │   └── router/        # Configuración de rutas
│   └── package.json
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfiles
└── docs/
    └── README.md
```

## 📝 Guías de Desarrollo

### Crear un nuevo modelo Django

1. Define el modelo en `apps/<modulo>/models.py`
2. Crea las migraciones: `python manage.py makemigrations`
3. Aplica las migraciones: `python manage.py migrate`
4. Crea el serializer en `apps/<modulo>/serializers.py`
5. Implementa las vistas en `apps/<modulo>/views.py`
6. Registra las URLs en `apps/<modulo>/urls.py`

### Crear un nuevo componente Vue

1. Crea el archivo en `frontend/src/components/`
2. Usa la Composition API con `<script setup>`
3. Aplica estilos con Tailwind CSS
4. Importa y usa el componente donde sea necesario

### Trabajar con WebSockets

1. Define los consumers en `apps/chat/consumers.py`
2. Registra las rutas WebSocket en `apps/chat/routing.py`
3. En el frontend, usa Socket.io-client para conectar
4. Implementa los eventos de emisión y escucha

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

## 📚 API Documentation

La documentación de la API está disponible en:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia Copyleft. Consulta el archivo `LICENSE` para más detalles.

## 👥 Equipo

- Desarrollo inicial por la comunidad Calicanto
- Mantenido por colaboradores voluntarios

## 📞 Contacto

- Email: contacto@calicanto.org
- Web: https://calicanto.org

---

*Construyendo comunidad, compartiendo hogar* 🏘️