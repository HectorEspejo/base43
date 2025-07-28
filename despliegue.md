# Guía de Despliegue de Calicanto en Ubuntu Server

Esta guía detalla el proceso completo para desplegar la plataforma Calicanto en un servidor Ubuntu 22.04 LTS o superior.

## Requisitos Previos

- Ubuntu Server 22.04 LTS o superior
- Mínimo 2GB RAM (recomendado 4GB)
- 20GB de espacio en disco
- Acceso root o usuario con privilegios sudo
- Dominio apuntando al servidor

## 1. Preparación del Sistema

### 1.1 Actualizar el Sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

### 1.2 Instalar Dependencias Base
```bash
# Python y herramientas de desarrollo
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip build-essential -y

# Base de datos
sudo apt install postgresql postgresql-contrib redis-server -y

# Servidor web y utilidades
sudo apt install nginx supervisor git curl wget -y

# Herramientas adicionales
sudo apt install libpq-dev libssl-dev libffi-dev -y
```

### 1.3 Instalar Node.js 18+
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
node --version  # Verificar instalación
```

## 2. Configuración de Base de Datos

### 2.1 PostgreSQL
```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE calicanto_db;
CREATE USER calicanto_user WITH PASSWORD '{V^8U4Tg04o-';
ALTER ROLE calicanto_user SET client_encoding TO 'utf8';
ALTER ROLE calicanto_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE calicanto_user SET timezone TO 'Europe/Madrid';

\q
```

### 2.2 Redis
```bash
# Verificar que Redis esté activo
sudo systemctl status redis-server
sudo systemctl enable redis-server
```

## 3. Configuración del Usuario y Aplicación

### 3.1 Crear Usuario del Sistema
```bash
sudo adduser calicanto --disabled-password --gecos "iSMeNOBrOcOS"
sudo usermod -aG www-data calicanto
```

### 3.2 Clonar el Proyecto
```bash
# Cambiar al usuario calicanto
sudo su - calicanto

# Clonar repositorio
cd ~
git clone [URL_DEL_REPOSITORIO] web
cd web
```

### 3.3 Configurar el Backend

```bash
# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
cd backend
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo de configuración
cp .env.example .env
```

Editar el archivo `.env` con los valores de producción:
```bash
nano .env
```

Contenido del `.env`:
```env
# Django Settings
SECRET_KEY=GENERAR_CLAVE_SEGURA_AQUI
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# PostgreSQL Database
POSTGRES_DB=calicanto_db
POSTGRES_USER=calicanto_user
POSTGRES_PASSWORD=CAMBIAR_PASSWORD_SEGURO
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# CORS Settings
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com

# Contact Admin Emails
CONTACT_ADMIN_EMAILS=calicanto.habitat@adobeverde.eu,admin@tu-dominio.com
```

### 3.4 Configurar Django
```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Crear directorios necesarios
mkdir -p media logs

# Salir del entorno virtual
deactivate
exit  # Volver a usuario con sudo
```

### 3.5 Construir el Frontend
```bash
sudo su - calicanto
cd ~/web/frontend

# Instalar dependencias
npm install

# Crear archivo de configuración de producción
cat > .env.production << EOF
VITE_API_URL=https://calicanto.adobeverde.eu
VITE_WS_URL=wss://calicanto.adobeverde.eu
EOF

# Construir para producción
npm run build

exit  # Volver a usuario con sudo
```

## 4. Configuración de Servicios

### 4.1 Gunicorn con Supervisor

Crear archivo de configuración:
```bash
sudo nano /etc/supervisor/conf.d/calicanto.conf
```

Contenido:
```ini
[group:calicanto]
programs=calicanto-gunicorn,calicanto-daphne,calicanto-celery,calicanto-celerybeat

[program:calicanto-gunicorn]
command=/home/calicanto/web/venv/bin/gunicorn core.wsgi:application --bind 127.0.0.1:8000 --workers 3 --timeout 120
directory=/home/calicanto/web/backend
user=calicanto
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/calicanto/web/logs/gunicorn.log
environment=PATH="/home/calicanto/web/venv/bin",LANG="es_ES.UTF-8",LC_ALL="es_ES.UTF-8"

[program:calicanto-daphne]
command=/home/calicanto/web/venv/bin/daphne -b 127.0.0.1 -p 8001 core.asgi:application
directory=/home/calicanto/web/backend
user=calicanto
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/calicanto/web/logs/daphne.log
environment=PATH="/home/calicanto/web/venv/bin",LANG="es_ES.UTF-8",LC_ALL="es_ES.UTF-8"

[program:calicanto-celery]
command=/home/calicanto/web/venv/bin/celery -A core worker -l info
directory=/home/calicanto/web/backend
user=calicanto
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/calicanto/web/logs/celery.log
environment=PATH="/home/calicanto/web/venv/bin",LANG="es_ES.UTF-8",LC_ALL="es_ES.UTF-8"

[program:calicanto-celerybeat]
command=/home/calicanto/web/venv/bin/celery -A core beat -l info
directory=/home/calicanto/web/backend
user=calicanto
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/calicanto/web/logs/celerybeat.log
environment=PATH="/home/calicanto/web/venv/bin",LANG="es_ES.UTF-8",LC_ALL="es_ES.UTF-8"
```

### 4.2 Configurar Nginx

Crear configuración del sitio:
```bash
sudo nano /etc/nginx/sites-available/calicanto
```

Contenido:
```nginx
# Redirigir HTTP a HTTPS
server {
    listen 80;
    server_name calicanto.adobeverde.eu www.calicanto.adobeverde.eu;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name calicanto.adobeverde.eu www.calicanto.adobeverde.eu
    
    # Seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Logs
    access_log /var/log/nginx/calicanto_access.log;
    error_log /var/log/nginx/calicanto_error.log;
    
    # Tamaño máximo de carga
    client_max_body_size 20M;
    
    # Frontend (Vue.js)
    location / {
        root /home/calicanto/web/frontend/dist;
        try_files $uri $uri/ /index.html;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
    
    # API Backend
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }
    
    # WebSocket para Chat
    location /ws {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }
    
    # Archivos estáticos de Django
    location /static {
        alias /home/calicanto/web/backend/staticfiles;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Archivos multimedia
    location /media {
        alias /home/calicanto/web/backend/media;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Documentación API
    location /api/docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $http_host;
    }
    
    # Django Admin
    location /admin {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # CKEditor
    location /ckeditor {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4.3 Activar Configuración
```bash
# Crear enlace simbólico
sudo ln -s /etc/nginx/sites-available/calicanto /etc/nginx/sites-enabled/

# Deshabilitar sitio por defecto
sudo rm /etc/nginx/sites-enabled/default

# Verificar configuración
sudo nginx -t

# Recargar Nginx
sudo systemctl reload nginx
```

## 5. Certificado SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d calicanto.adobeverde.eu -d www.calicanto.adobeverde.eu

# Configurar renovación automática
sudo systemctl enable certbot.timer
```

## 6. Configuración del Firewall

```bash
# Configurar UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
sudo ufw status
```

## 7. Iniciar Servicios

```bash
# Recargar supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Iniciar todos los servicios
sudo supervisorctl start calicanto:*

# Verificar estado
sudo supervisorctl status

# Reiniciar servicios
sudo systemctl restart nginx
sudo systemctl restart redis-server
sudo systemctl restart postgresql
```

## 8. Monitoreo y Logs

### 8.1 Ver logs en tiempo real
```bash
# Logs de Gunicorn
sudo tail -f /home/calicanto/web/logs/gunicorn.log

# Logs de Nginx
sudo tail -f /var/log/nginx/calicanto_error.log

# Logs de Supervisor
sudo tail -f /var/log/supervisor/supervisord.log
```

### 8.2 Comandos útiles de Supervisor
```bash
# Ver estado de todos los procesos
sudo supervisorctl status

# Reiniciar un servicio específico
sudo supervisorctl restart calicanto-gunicorn

# Detener todos los servicios
sudo supervisorctl stop calicanto:*

# Iniciar todos los servicios
sudo supervisorctl start calicanto:*
```

## 9. Mantenimiento

### 9.1 Actualizar la Aplicación
```bash
# Como usuario calicanto
sudo su - calicanto
cd ~/web

# Actualizar código
git pull origin main

# Backend
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
deactivate

# Frontend
cd ../frontend
npm install
npm run build

exit

# Reiniciar servicios
sudo supervisorctl restart calicanto:*
```

### 9.2 Backup de Base de Datos
```bash
# Crear directorio de backups
sudo mkdir -p /var/backups/calicanto
sudo chown calicanto:calicanto /var/backups/calicanto

# Script de backup (crear como /home/calicanto/backup.sh)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/calicanto"
DB_NAME="calicanto_db"
DB_USER="calicanto_user"

# Backup de base de datos
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Backup de archivos media
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz -C /home/calicanto/web/backend media/

# Eliminar backups antiguos (más de 7 días)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### 9.3 Cron para Backups Automáticos
```bash
# Editar crontab del usuario calicanto
sudo -u calicanto crontab -e

# Agregar línea para backup diario a las 3 AM
0 3 * * * /home/calicanto/backup.sh
```

## 10. Solución de Problemas

### 10.1 Error 502 Bad Gateway
- Verificar que Gunicorn esté ejecutándose: `sudo supervisorctl status`
- Revisar logs: `sudo tail -f /home/calicanto/web/logs/gunicorn.log`
- Verificar permisos de archivos

### 10.2 Archivos estáticos no cargan
- Verificar que se ejecutó `collectstatic`
- Revisar permisos del directorio staticfiles
- Verificar configuración de Nginx

### 10.3 WebSocket no funciona
- Verificar que Daphne esté ejecutándose
- Revisar configuración de proxy en Nginx
- Verificar que Redis esté activo

### 10.4 Permisos de archivos
```bash
# Arreglar permisos
sudo chown -R calicanto:www-data /home/calicanto/web
sudo chmod -R 755 /home/calicanto/web
sudo chmod -R 775 /home/calicanto/web/backend/media
sudo chmod -R 775 /home/calicanto/web/backend/logs
```

## Notas Importantes

1. **Seguridad**: Siempre use contraseñas seguras y únicas
2. **Backups**: Configure backups automáticos regulares
3. **Monitoreo**: Considere instalar herramientas como Prometheus o Netdata
4. **Actualizaciones**: Mantenga el sistema y dependencias actualizadas
5. **HTTPS**: Nunca ejecute en producción sin SSL/TLS

## Contacto y Soporte

Para soporte técnico o consultas sobre el despliegue:
- Email: calicanto.habitat@adobeverde.eu
- Documentación: [URL de documentación]