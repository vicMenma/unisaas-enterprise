
# RBAC Policy (Strict)

## Roles
- owner
- university_admin
- registration
- examination
- teacher
- student

## Enforcement
- API level permissions
- Object-level permissions

## Rules
- student: own data only
- teacher: assigned courses
- registration: student CRUD
- examination: grades control
