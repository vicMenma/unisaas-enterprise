# API

Base path: `/api/v1/`

Tenant resolution:

- Preferred: `X-Tenant-Slug: demo`
- Alternative: tenant subdomain, such as `demo.example.com`

Authentication:

- `POST /api/v1/auth/login/`
- `POST /api/v1/auth/refresh/`
- `GET /api/v1/auth/me/`

Main resources:

- Academic: `/academic-years/`, `/faculties/`, `/departments/`, `/programmes/`, `/semesters/`, `/courses/`, `/course-allocations/`
- Students: `/students/`, `/students/me/`
- Registration: `/enrollments/`, `/enrollment-courses/`
- Examinations: `/grades/`, `/grades/{id}/approve/`, `/grades/gpa/{enrollment_id}/`, `/grades/transcript/{student_id}/`
- Finance: `/fee-categories/`, `/invoices/`, `/payments/`, `/payments/{id}/receipt/`
- Admissions: `/applications/`, `/applications/{id}/accept/`, `/applications/{id}/reject/`, `/documents/`, `/documents/{id}/verify/`
- Audit: `/audit-logs/`
- Notifications: `/notifications/`, `/notifications/{id}/read/`, `/notifications/read-all/`, `/notifications/unread-count/`

Roles:

- `owner`, `university_admin`: administration across the tenant.
- `registration`: students, registration, admissions, and finance operations.
- `examination`, `teacher`: grade and transcript workflows.
- `student`: own student portal and notifications.
