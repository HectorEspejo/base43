# Deploying Calicanto on Coolify

This guide explains how to deploy the Calicanto project on Coolify.

## Prerequisites

1. A Coolify instance installed and running
2. A domain name (optional but recommended)
3. Access to Coolify dashboard

## Deployment Steps

### 1. Create a New Project in Coolify

1. Log in to your Coolify dashboard
2. Click on "New Project"
3. Give your project a name (e.g., "Calicanto")

### 2. Add a New Service

1. In your project, click "New Service"
2. Select "Docker Compose" as the service type
3. Choose your deployment server

### 3. Configure the Service

#### Git Repository
- Repository URL: Your Git repository URL
- Branch: `main` (or your preferred branch)
- Build Path: `/`

#### Docker Compose Configuration
1. Select "Custom Docker Compose"
2. Use the file: `docker-compose.prod.yml`

### 4. Environment Variables

In Coolify's environment variables section, add the following:

```bash
# PostgreSQL
POSTGRES_DB=calicanto_db
POSTGRES_USER=calicanto_user
POSTGRES_PASSWORD=<generate-secure-password>

# Redis
REDIS_PASSWORD=<generate-secure-password>

# Django
SECRET_KEY=<generate-long-random-string>
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Frontend
VITE_API_URL=https://your-domain.com/api
```

### 5. Persistent Storage

Configure persistent volumes in Coolify:

1. **PostgreSQL Data**: `/var/lib/postgresql/data`
2. **Redis Data**: `/data`
3. **Media Files**: `/app/media`
4. **Static Files**: `/app/staticfiles`

### 6. Domain Configuration

1. In Coolify, go to the "Domains" section
2. Add your domain (e.g., `your-domain.com`)
3. Coolify will automatically handle SSL certificates with Let's Encrypt

### 7. Deploy

1. Click "Deploy" in Coolify
2. Monitor the deployment logs
3. Wait for all services to be healthy

### 8. Post-Deployment

After successful deployment:

1. **Create Django Superuser**:
   ```bash
   # Access the backend container through Coolify's terminal
   python manage.py createsuperuser
   ```

2. **Run Initial Migrations** (if needed):
   ```bash
   python manage.py migrate
   ```

3. **Collect Static Files** (if not done automatically):
   ```bash
   python manage.py collectstatic --noinput
   ```

## Alternative: Using Coolify's Docker Registry

If you prefer to use Coolify's built-in Docker registry:

1. Build and push images to Coolify's registry
2. Update `docker-compose.prod.yml` to use the registry images:
   ```yaml
   backend:
     image: registry.your-coolify-domain.com/calicanto-backend:latest
   
   nginx:
     image: registry.your-coolify-domain.com/calicanto-frontend:latest
   ```

## Monitoring

Coolify provides built-in monitoring:
- Container logs
- Resource usage
- Health checks
- Automatic restarts

## Backup Strategy

1. **Database Backups**: Configure automatic PostgreSQL backups in Coolify
2. **Media Files**: Set up regular backups of the media volume
3. **Redis**: Optional, as it's mainly used for caching

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check PostgreSQL container is running
   - Verify environment variables are set correctly

2. **Static Files Not Loading**
   - Ensure `collectstatic` has run
   - Check nginx configuration for static file paths

3. **WebSocket Connection Failed**
   - Verify nginx WebSocket proxy configuration
   - Check Redis connection for Django Channels

### Logs

Access logs through Coolify's interface:
- Backend logs: Django application logs
- Nginx logs: Access and error logs
- PostgreSQL logs: Database queries and errors

## Security Considerations

1. **Environment Variables**: Keep all sensitive data in Coolify's encrypted environment variables
2. **SSL**: Always use HTTPS in production
3. **Firewall**: Configure Coolify's firewall rules appropriately
4. **Updates**: Enable automatic updates in Coolify for security patches

## Scaling

To scale your application:

1. **Horizontal Scaling**: Add more backend workers in docker-compose
2. **Database**: Consider using Coolify's managed PostgreSQL for better performance
3. **Caching**: Utilize Redis for session storage and caching

## Support

For issues specific to:
- **Coolify**: Check [Coolify documentation](https://coolify.io/docs)
- **Calicanto**: Refer to the project documentation