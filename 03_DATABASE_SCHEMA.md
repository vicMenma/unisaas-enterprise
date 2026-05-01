
# Database Schema (Production)

## Global Rule
Each table includes:
- id (UUID PK)
- university_id (FK, indexed)

---

## universities
- id: UUID
- name: string
- slug: unique
- matricule_prefix: string
- matricule_pattern: JSONB
- subscription_plan
- created_at

---

## users
- id
- university_id
- email (unique per tenant)
- role
- password_hash
- is_active

---

## student_profiles
- id
- user_id (1-1)
- university_id
- matricule (unique)
- program_id
- status
- entry_year
- current_level

Indexes:
- (university_id, matricule)
- (university_id, email)
