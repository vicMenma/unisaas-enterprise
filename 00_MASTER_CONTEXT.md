
# MASTER CONTEXT — UniSaaS (Production)

## System Nature
Multi-tenant SaaS University Management System.

## Non-Negotiable Constraints
- Strict tenant isolation (no cross-tenant reads EVER)
- PostgreSQL is source of truth
- All writes must be atomic where needed
- No silent failures

## Architecture Rules
- Modular monolith (Django apps)
- No microservices initially
- Each app owns its models

## Data Rules
- Every model has university_id
- UUID primary keys only
- Academic data is append-only

## Security
- JWT authentication
- RBAC enforced at:
  - View level
  - Object level

## Developer Behavior (Claude)
- NEVER invent schema
- NEVER skip validation
- ASK if missing info
