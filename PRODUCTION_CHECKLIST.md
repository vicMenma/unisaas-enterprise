# 🚀 UniSaaS Production Deployment Checklist

Follow this guide to move UniSaaS from your local machine to a live university environment.

## 1. Environment Security
Ensure your `.env` file on the server contains these production values:
- `DEBUG=False`
- `SECRET_KEY`= (Generate a 50+ character random string)
- `ALLOWED_HOSTS=youruniversity.com,api.youruniversity.com`
- `DATABASE_URL=postgres://user:password@db:5432/unisaas`
- `CELERY_BROKER_URL=redis://redis:6379/0`

## 2. SSL & Domain
Use Nginx as a reverse proxy.
- Port 8000 (Django) should be proxied through Nginx.
- Use **Certbot (Let's Encrypt)** for free SSL certificates.

## 3. Database Persistence
In `docker-compose.yml`, ensure the postgres volume is mapped to a secure location on the host:
```yaml
volumes:
  - /var/lib/unisaas/postgres_data:/var/lib/postgresql/data/
```

## 4. Static Files
In production, Django does not serve static files. Run:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```
Then configure Nginx to serve the `/static/` folder.

## 5. Monitoring
- Use **Sentry** for error tracking.
- Use **Prometheus/Grafana** for server health monitoring.
