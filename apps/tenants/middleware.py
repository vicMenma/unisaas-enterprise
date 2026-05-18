from django.conf import settings
from django.db.utils import DatabaseError, OperationalError, ProgrammingError
from django.http import JsonResponse
from ipaddress import ip_address

from apps.tenants.models import University


class TenantMiddleware:
    """Resolve the active university from header, subdomain, or demo fallback."""

    header_name = "X-Tenant-Slug"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_slug = self._tenant_slug_from_request(request)
        request.tenant = None

        if tenant_slug:
            try:
                request.tenant = University.objects.get(slug=tenant_slug)
            except University.DoesNotExist:
                return JsonResponse({"error": "Invalid tenant specified"}, status=400)
        elif getattr(settings, "ENABLE_DEMO_TENANT", False):
            try:
                request.tenant = University.objects.filter(
                    slug=getattr(settings, "DEMO_TENANT_SLUG", "demo"),
                ).first()
            except (DatabaseError, OperationalError, ProgrammingError):
                request.tenant = None

        return self.get_response(request)

    def _tenant_slug_from_request(self, request):
        header_slug = request.headers.get(self.header_name)
        if header_slug:
            return header_slug.strip().lower()

        host = request.get_host().split(":")[0].lower()
        if host == "localhost" or self._is_ip_address(host):
            return None

        for parent_domain in self._tenant_parent_domains():
            if host == parent_domain:
                return None
            suffix = f".{parent_domain}"
            if host.endswith(suffix):
                subdomain = host[: -len(suffix)].strip(".")
                if subdomain and subdomain not in {"www", "api"}:
                    return subdomain.split(".")[0]
        return None

    def _tenant_parent_domains(self):
        return [
            domain.strip().lower().lstrip(".")
            for domain in getattr(settings, "TENANT_PARENT_DOMAINS", [])
            if domain.strip()
        ]

    def _is_ip_address(self, host):
        try:
            ip_address(host)
        except ValueError:
            return False
        return True
