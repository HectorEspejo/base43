# Base43 Deployment Guide

This guide covers deploying Base43 to production environments.

## Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Domain name pointing to your server
- SSL certificate (Let's Encrypt recommended)
- At least 2GB RAM
- 20GB+ storage

## Production Deployment Steps

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib \
    redis-server \
    nginx \
    supervisor \
    git \
    certbot python3-certbot-nginx
```

### 2. Create Application User

```bash
sudo adduser base43 --disabled-password
sudo usermod -aG www-data base43
```

### 3. Clone Repository

```bash
sudo su - base43
git clone https://github.com/your-repo/base43.git
cd base43
```

### 4. Backend Setup

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install gunicorn

# Create production settings
cp .env.example .env
# Edit .env with production values
```

### 5. Database Setup

```bash
# As postgres user
sudo -u postgres psql

CREATE DATABASE base43_db;
CREATE USER base43_user WITH PASSWORD 'secure_password';
ALTER ROLE base43_user SET client_encoding TO 'utf8';
ALTER ROLE base43_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE base43_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE base43_db TO base43_user;
\q

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. Frontend Build

```bash
cd ../frontend
npm install
npm run build
```

### 7. Supervisor Configuration

Create `/etc/supervisor/conf.d/base43.conf`:

```ini
[program:base43-gunicorn]
command=/home/base43/base43/venv/bin/gunicorn core.wsgi:application --bind 127.0.0.1:8000 --workers 3
directory=/home/base43/base43/backend
user=base43
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/base43/gunicorn.log
environment=PATH="/home/base43/base43/venv/bin"

[program:base43-daphne]
command=/home/base43/base43/venv/bin/daphne -b 127.0.0.1 -p 8001 core.asgi:application
directory=/home/base43/base43/backend
user=base43
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/base43/daphne.log

[program:base43-celery]
command=/home/base43/base43/venv/bin/celery -A core worker -l info
directory=/home/base43/base43/backend
user=base43
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/base43/celery.log
```

### 8. Nginx Configuration

Create `/etc/nginx/sites-available/base43`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    client_max_body_size 10M;
    
    # Frontend
    location / {
        root /home/base43/base43/frontend/dist;
        try_files $uri $uri/ /index.html;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
    
    # API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket
    location /ws {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Static files
    location /static {
        alias /home/base43/base43/backend/staticfiles;
        expires 30d;
    }
    
    # Media files
    location /media {
        alias /home/base43/base43/backend/media;
        expires 7d;
    }
    
    # Admin
    location /admin {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 9. Enable Site and SSL

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/base43 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 10. Start Services

```bash
# Create log directory
sudo mkdir -p /var/log/base43
sudo chown base43:base43 /var/log/base43

# Start services
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

## Docker Deployment (Alternative)

### 1. Create docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: base43_db
      POSTGRES_USER: base43_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    command: redis-server --requirepass ${REDIS_PASSWORD}

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://base43_user:${POSTGRES_PASSWORD}@postgres:5432/base43_db
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    volumes:
      - frontend_dist:/app/dist

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - frontend_dist:/var/www/frontend
      - static_volume:/var/www/static
      - media_volume:/var/www/media
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
  static_volume:
  media_volume:
  frontend_dist:
```

### 2. Backend Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 3. Frontend Dockerfile

```dockerfile
FROM node:18 as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

## Monitoring and Maintenance

### Health Checks

Add health check endpoint to Django:

```python
# urls.py
path('health/', lambda request: JsonResponse({'status': 'ok'})),
```

### Backup Strategy

Create backup script `/home/base43/backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/base43"

# Database backup
pg_dump -U base43_user base43_db > $BACKUP_DIR/db_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C /home/base43/base43/backend media/

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Add to crontab:
```bash
0 3 * * * /home/base43/backup.sh
```

### Monitoring Tools

Consider installing:
- Prometheus + Grafana for metrics
- Sentry for error tracking
- ELK Stack for log analysis

## Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **Secret Keys**: Use strong, unique secret keys
3. **Database**: Use strong passwords, limit connections
4. **Firewall**: Configure UFW or iptables
5. **Updates**: Keep system and dependencies updated
6. **HTTPS**: Always use SSL in production
7. **Headers**: Configure security headers in Nginx

## Performance Optimization

1. **Caching**: Configure Redis caching in Django
2. **Database**: Add indexes, optimize queries
3. **Static Files**: Use CDN for static assets
4. **Compression**: Enable gzip in Nginx
5. **Load Balancing**: Use multiple Gunicorn workers

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**: Check if Gunicorn is running
2. **Static files not loading**: Run `collectstatic`
3. **Database connection errors**: Check credentials and permissions
4. **WebSocket not working**: Ensure Daphne is running

### Logs

Check logs at:
- `/var/log/base43/gunicorn.log`
- `/var/log/nginx/error.log`
- `/var/log/supervisor/supervisord.log`

## Scaling

For high traffic:
1. Use multiple application servers
2. Implement database replication
3. Use Redis Cluster
4. Add CDN (CloudFlare, AWS CloudFront)
5. Implement horizontal scaling with Kubernetes