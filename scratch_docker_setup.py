import os

# Dockerfile for Django app
DOCKERFILE = """
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "unisaas.wsgi:application"]
"""

# docker-compose.yml
DOCKER_COMPOSE = """
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=unisaas
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  redis:
    image: redis:7-alpine

  web:
    build: .
    command: python manage.py migrate && python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - SECRET_KEY=dev_key_only
      - DATABASE_URL=postgres://postgres:postgres@db:5432/unisaas
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery:
    build: .
    command: celery -A unisaas worker -l info
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/unisaas
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
      - web

volumes:
  postgres_data:
"""

with open('Dockerfile', 'w') as f:
    f.write(DOCKERFILE.strip())

with open('docker-compose.yml', 'w') as f:
    f.write(DOCKER_COMPOSE.strip())
