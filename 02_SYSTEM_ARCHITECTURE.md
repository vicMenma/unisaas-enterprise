
# System Architecture

## Pattern
Modular monolith

## Layers
1. Client (React / Mobile)
2. Gateway (Nginx)
3. Django App Layer
4. Async (Celery + Redis)
5. Database (PostgreSQL)

## Core Apps
- tenants
- accounts
- students
- academic
- registration
- examinations
- audit

## Rules
- No direct DB access from outside Django ORM
- Services layer for business logic
- Serializers only validate data
