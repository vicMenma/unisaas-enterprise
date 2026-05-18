# Architecture

UniSaaS Enterprise is a Django modular monolith. Domain apps live under `apps/` but keep stable Django app labels so migrations remain compatible.

Core modules:

- `tenants`: universities and tenant base model.
- `accounts`: custom user, JWT login, roles, and profile endpoint.
- `academic`: faculties, departments, programmes, courses, semesters, academic years, and course allocations.
- `students`: student profiles, matricule generation, and student portal API.
- `registration`: semester enrollment and enrolled courses.
- `examinations`: grades, GPA, transcript PDF, and grade locking.
- `finance`: fee categories, invoices, payments, balances, and receipts.
- `admissions`: applications, documents, admission decisions, offer letters.
- `audit`: append-only audit trail.
- `notifications`: in-app notifications.

Tenant isolation is enforced through `TenantMiddleware`, tenant-scoped permissions, and serializer querysets that restrict foreign keys to the active university.
