
# API Contract (Production)

## Auth
POST /api/auth/login
POST /api/auth/refresh

## Students
POST /api/students/
GET /api/students/
GET /api/students/{id}

## Enrollment
POST /api/enrollments/

## Exams
POST /api/grades/
GET /api/results/

## Rules
- All endpoints require JWT
- Tenant resolved via middleware
- Pagination mandatory
