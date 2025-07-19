# Gu�a de Despliegue en Producci�n - Proyecto Calicanto

Esta gu�a detalla el proceso completo para desplegar el proyecto Calicanto (Django + Vue.js) en un servidor Ubuntu.

## Requisitos Previos

- Servidor Ubuntu 20.04 LTS o superior
- Acceso SSH con privilegios sudo
- Dominio apuntando al servidor (opcional pero recomendado)
- Al menos 2GB de RAM y 20GB de espacio en disco

## 1. Preparaci�n del Servidor

### 1.1 Actualizar el sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Instalar dependencias del sistema

```bash
sudo apt install -y python3-pip python3-dev python3-venv \
    nginx postgresql postgresql-contrib \
    redis-server supervisor \
    git curl build-essential \
    libpq-dev libssl-dev libffi-dev \
    libjpeg-dev zlib1g-dev
```

### 1.3 Instalar Node.js (para el frontend)

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

## 2. Configuraci�n de PostgreSQL

### 2.1 Crear base de datos y usuario

```bash
sudo -u postgres psql

# Dentro de PostgreSQL:
CREATE DATABASE calicanto_db;
CREATE USER calicanto_user WITH PASSWORD 'tu_password_segura';
ALTER ROLE calicanto_user SET client_encoding TO 'utf8';
ALTER ROLE calicanto_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE calicanto_user SET timezone TO 'Europe/Madrid';
GRANT ALL PRIVILEGES ON DATABASE calicanto_db TO calicanto_user;
\q
```

## 3. Configuraci�n del Proyecto

### 3.1 Crear usuario para la aplicaci�n

```bash
sudo adduser --system --group calicanto
sudo mkdir -p /home/calicanto
sudo chown calicanto:calicanto /home/calicanto
```

### 3.2 Clonar el repositorio

```bash
sudo -u calicanto git clone https://github.com/tu-usuario/calicanto.git /home/calicanto/web
cd /home/calicanto/web
```

### 3.3 Crear entorno virtual Python

```bash
sudo -u calicanto python3 -m venv /home/calicanto/venv
```

## 4. Configuraci�n del Backend (Django)

### 4.1 Crear archivo de configuraci�n de producci�n

```bash
sudo -u calicanto nano /home/calicanto/web/backend/.env
```

Contenido del archivo `.env`:

```env
# Django settings
SECRET_KEY=genera_una_clave_secreta_muy_larga_y_aleatoria
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,dev-calicanto-072025.4d3.org,www.dev-calicanto-072025.4d3.org

# Database
DATABASE_URL=postgres://calicanto_user:tu_password_segura@localhost/calicanto_db

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion

# Security
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=https://dev-calicanto-072025.4d3.org,https://www.dev-calicanto-072025.4d3.org
```

### 4.2 Instalar dependencias Python

```bash
sudo -u calicanto /home/calicanto/venv/bin/pip install --upgrade pip
sudo -u calicanto /home/calicanto/venv/bin/pip install -r /home/calicanto/web/backend/requirements.txt
sudo -u calicanto /home/calicanto/venv/bin/pip install gunicorn
sudo -u calicanto /home/calicanto/venv/bin/pip install channels channels-redis daphne
```

### 4.3 Crear archivos necesarios para Celery

```bash
# Crear archivo celery.py
sudo -u calicanto nano /home/calicanto/web/backend/core/celery.py
```

Contenido del archivo:
```python
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

```bash
# Actualizar __init__.py
sudo -u calicanto nano /home/calicanto/web/backend/core/__init__.py
```

Contenido:
```python
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### 4.4 Configurar Django para producci�n

```bash
# Recolectar archivos est�ticos
sudo -u calicanto /home/calicanto/venv/bin/python /home/calicanto/web/backend/manage.py collectstatic --noinput

# Ejecutar migraciones
sudo -u calicanto /home/calicanto/venv/bin/python /home/calicanto/web/backend/manage.py migrate

# Crear superusuario
sudo -u calicanto /home/calicanto/venv/bin/python /home/calicanto/web/backend/manage.py createsuperuser

# Crear directorios para media y logs
sudo mkdir -p /home/calicanto/web/backend/media
sudo mkdir -p /var/log/calicanto
sudo chown -R calicanto:calicanto /home/calicanto/web/backend/media
sudo chown -R calicanto:calicanto /var/log/calicanto
```

## 5. Configuraci�n del Frontend (Vue.js)

### 5.1 Instalar dependencias y construir

```bash
cd /home/calicanto/web/frontend
sudo -u calicanto npm install
sudo -u calicanto npm run build
```

### 5.2 Crear archivo de configuraci�n para producci�n

Editar `/home/calicanto/web/frontend/.env.production`:

```env
VITE_API_URL=https://dev-calicanto-072025.4d3.org/api
```

## 6. Configuraci�n de Gunicorn

### 6.1 Crear archivo de configuraci�n

```bash
sudo nano /etc/supervisor/conf.d/calicanto.conf
```

Contenido:

```ini
[program:calicanto]
command=/home/calicanto/venv/bin/gunicorn core.wsgi:application --bind unix:/home/calicanto/web/calicanto.sock --workers 3 --timeout 120
directory=/home/calicanto/web/backend
user=calicanto
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/calicanto/gunicorn.log
environment=PATH="/home/calicanto/venv/bin",DJANGO_SETTINGS_MODULE="core.settings"
```

### 6.2 Crear directorio de logs

```bash
sudo mkdir -p /var/log/calicanto
sudo chown calicanto:calicanto /var/log/calicanto
```

## 7. Configuraci�n de Daphne (para WebSockets)

### 7.1 Crear configuraci�n de Daphne

```bash
sudo nano /etc/supervisor/conf.d/calicanto-asgi.conf
```

Contenido:

```ini
[program:calicanto-asgi]
command=/home/calicanto/venv/bin/daphne -u /home/calicanto/web/daphne.sock core.asgi:application
directory=/home/calicanto/web/backend
user=calicanto
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
redirect_stderr=true
stdout_logfile=/var/log/calicanto/daphne.log
stderr_logfile=/var/log/calicanto/daphne.error.log
environment=PATH="/home/calicanto/venv/bin:/usr/local/bin:/usr/bin:/bin",PYTHONPATH="/home/calicanto/web/backend",DJANGO_SETTINGS_MODULE="core.settings"
```

## 8. Configuraci�n de Celery (para tareas as�ncronas)

### 8.1 Crear configuraci�n de Celery

```bash
sudo nano /etc/supervisor/conf.d/celery.conf
```

Contenido:

```ini
[program:celery]
command=/home/calicanto/venv/bin/celery -A core worker -l info
directory=/home/calicanto/web/backend
user=calicanto
numprocs=1
stdout_logfile=/var/log/calicanto/celery.log
stderr_logfile=/var/log/calicanto/celery.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
environment=PATH="/home/calicanto/venv/bin",PYTHONPATH="/home/calicanto/web/backend",DJANGO_SETTINGS_MODULE="core.settings"

[program:celery-beat]
command=/home/calicanto/venv/bin/celery -A core beat -l info
directory=/home/calicanto/web/backend
user=calicanto
numprocs=1
stdout_logfile=/var/log/calicanto/celery-beat.log
stderr_logfile=/var/log/calicanto/celery-beat.log
autostart=true
autorestart=true
environment=PATH="/home/calicanto/venv/bin",PYTHONPATH="/home/calicanto/web/backend",DJANGO_SETTINGS_MODULE="core.settings"
```

## 9. Configuraci�n de Nginx

### 9.1 Crear configuraci�n del sitio

```bash
sudo nano /etc/nginx/sites-available/calicanto
```

Contenido:

```nginx
upstream calicanto_backend {
    server unix:/home/calicanto/web/calicanto.sock;
}

server {
    listen 80;
    server_name dev-calicanto-072025.4d3.org www.dev-calicanto-072025.4d3.org;
    
    # Redirecci�n a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dev-calicanto-072025.4d3.org www.dev-calicanto-072025.4d3.org;
    
    # SSL Configuration (usar Certbot para obtener certificados)
    ssl_certificate /etc/letsencrypt/live/dev-calicanto-072025.4d3.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dev-calicanto-072025.4d3.org/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline' 'unsafe-eval'" always;
    
    # Frontend (Vue.js)
    location / {
        root /home/calicanto/web/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://calicanto_backend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        client_max_body_size 100M;
    }
    
    # Django Admin
    location /admin {
        proxy_pass http://calicanto_backend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Static files (Django)
    location /static/ {
        alias /home/calicanto/web/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /home/calicanto/web/backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # WebSocket support (Daphne on port 8001)
    location /ws {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # CKEditor uploads
    location /ckeditor/ {
        proxy_pass http://calicanto_backend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # API Documentation
    location ~ ^/api/(docs|redoc)/ {
        proxy_pass http://calicanto_backend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 9.2 Activar el sitio

```bash
sudo ln -s /etc/nginx/sites-available/calicanto /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9.3 Nota importante sobre Nginx

Cuando uses Let's Encrypt (Certbot) para SSL, este modificar� autom�ticamente tu configuraci�n de Nginx. Despu�s de ejecutar Certbot, verifica que la configuraci�n de WebSocket siga apuntando a `http://127.0.0.1:8001` y no a `http://calicanto_backend`.

## 10. Configuraci�n SSL con Let's Encrypt

### 10.1 Configuraci�n inicial (HTTP)

Primero, crea una configuraci�n temporal solo con HTTP:

```bash
sudo nano /etc/nginx/sites-available/calicanto
```

Contenido temporal:
```nginx
upstream calicanto_backend {
    server unix:/home/calicanto/web/calicanto.sock;
}

server {
    listen 80;
    server_name dev-calicanto-072025.4d3.org www.dev-calicanto-072025.4d3.org;
    
    # Frontend (Vue.js)
    location / {
        root /home/calicanto/web/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://calicanto_backend;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### 10.2 Instalar y ejecutar Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d dev-calicanto-072025.4d3.org -d www.dev-calicanto-072025.4d3.org
```

### 10.3 Actualizar configuraci�n despu�s de SSL

Despu�s de que Certbot configure SSL, actualiza la configuraci�n completa con todas las rutas necesarias.

## 11. Configuraci�n de Daphne para WebSockets

### 11.1 Cambiar Daphne a puerto TCP

Para mejor compatibilidad, configura Daphne para usar TCP en lugar de socket Unix:

```bash
sudo nano /etc/supervisor/conf.d/calicanto-asgi.conf
```

Actualizar el comando:
```ini
command=/home/calicanto/venv/bin/daphne -b 127.0.0.1 -p 8001 core.asgi:application
```

## 12. Iniciar servicios

```bash
# Recargar supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Iniciar aplicaciones
sudo supervisorctl start calicanto
sudo supervisorctl start calicanto-asgi
sudo supervisorctl start celery
sudo supervisorctl start celery-beat

# Verificar estado
sudo supervisorctl status
```

## 13. Configuraci�n del Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 14. Monitoreo y Logs

### 14.1 Ver logs de la aplicaci�n

```bash
# Logs de Gunicorn
sudo tail -f /var/log/calicanto/gunicorn.log

# Logs de Daphne (WebSockets)
sudo tail -f /var/log/calicanto/daphne.log

# Logs de Celery
sudo tail -f /var/log/calicanto/celery.log

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### 14.2 Monitorear procesos

```bash
# Ver estado de supervisor
sudo supervisorctl status

# Ver uso de recursos
htop
```

## 15. Backup y Mantenimiento

### 15.1 Script de backup de base de datos

Crear `/home/calicanto/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/home/calicanto/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="calicanto_db"

mkdir -p $BACKUP_DIR
pg_dump -U calicanto_user -h localhost $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Eliminar backups antiguos (m�s de 30 d�as)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

### 15.2 Programar backup autom�tico

```bash
sudo crontab -e
# Agregar:
0 2 * * * /home/calicanto/backup.sh
```

## 16. Actualizaci�n del C�digo

Para actualizar la aplicaci�n:

```bash
# Backend
cd /home/calicanto/web
sudo -u calicanto git pull origin main
sudo -u calicanto /home/calicanto/venv/bin/pip install -r backend/requirements.txt
sudo -u calicanto /home/calicanto/venv/bin/python backend/manage.py migrate
sudo -u calicanto /home/calicanto/venv/bin/python backend/manage.py collectstatic --noinput

# Frontend
cd /home/calicanto/web/frontend
sudo -u calicanto npm install
sudo -u calicanto npm run build

# Reiniciar servicios
sudo supervisorctl restart calicanto
sudo supervisorctl restart calicanto-asgi
sudo supervisorctl restart celery
sudo systemctl reload nginx
```

## 17. Soluci�n de Problemas Comunes

### Error 502 Bad Gateway
- Verificar que Gunicorn est� ejecut�ndose: `sudo supervisorctl status calicanto`
- Revisar logs: `sudo tail -f /var/log/calicanto/gunicorn.log`
- Verificar permisos del socket: `ls -la /home/calicanto/web/`

### Archivos est�ticos no se cargan
- Verificar que se ejecut� `collectstatic`
- Revisar permisos: `ls -la /home/calicanto/web/backend/staticfiles/`
- Verificar configuraci�n de Nginx

### Base de datos no conecta
- Verificar credenciales en `.env`
- Probar conexi�n: `sudo -u postgres psql -U calicanto_user -d calicanto_db`

### WebSockets no funcionan
- Verificar que Daphne est� ejecut�ndose: `sudo supervisorctl status calicanto-asgi`
- Revisar logs: `sudo tail -f /var/log/calicanto/daphne.log`
- Verificar que Nginx redirija `/ws` a `http://127.0.0.1:8001`
- Asegurarse de que el frontend env�e el token JWT en la URL del WebSocket

### Panel admin sin estilos CSS
- Ejecutar collectstatic: `sudo -u calicanto /home/calicanto/venv/bin/python /home/calicanto/web/backend/manage.py collectstatic --noinput`
- Verificar permisos: `ls -la /home/calicanto/web/backend/staticfiles/`
- Revisar configuraci�n de Nginx para `/static/`

### Error con Celery
- Verificar que los archivos `celery.py` y `__init__.py` est�n correctamente configurados
- Revisar logs: `sudo tail -f /var/log/calicanto/celery.log`
- Asegurarse de que Redis est� funcionando: `redis-cli ping`

## Notas Finales

- Mantener el sistema actualizado regularmente
- Monitorear el uso de recursos del servidor
- Configurar alertas para errores cr�ticos
- Realizar backups peri�dicos de la base de datos y archivos media
- Revisar logs regularmente para detectar problemas