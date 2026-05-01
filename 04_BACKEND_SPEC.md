
# Backend Specification

## Stack
- Django 5
- DRF
- PostgreSQL
- Redis
- Celery

## Patterns
- Service layer for business logic
- Fat models NOT allowed
- Thin views

## Auth
- JWT via SimpleJWT

## Validation
- DRF serializers only

## Transactions
- Required for:
  - matricule generation
  - enrollment
  - grade submission
