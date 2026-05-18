# Security

Security defaults:

- Production refuses to start without `SECRET_KEY` and `ALLOWED_HOSTS`.
- `DEBUG` is always false in production settings.
- CORS is allow-list based in production.
- Secure cookies, HSTS, SSL redirect, content sniffing protection, and clickjacking protection are enabled in production.
- API access is tenant-scoped and role-scoped.
- Audit logs are append-only through API and model safeguards.

Operational guidance:

- Do not commit `.env`, database dumps, media uploads, or generated logs.
- Rotate `SECRET_KEY` and superuser credentials before live deployments.
- Keep `ENABLE_DEMO_TENANT=false` in production unless intentionally running a public demo.
