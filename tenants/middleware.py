from django.http import JsonResponse
from tenants.models import University

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # We look for a tenant slug in the headers (e.g. X-Tenant-Slug: harvard)
        # In a real app, this might come from the subdomain.
        tenant_slug = request.headers.get('X-Tenant-Slug')
        
        if tenant_slug:
            try:
                request.tenant = University.objects.get(slug=tenant_slug)
            except University.DoesNotExist:
                return JsonResponse({'error': 'Invalid tenant specified'}, status=400)
        else:
            # If no tenant is provided, we set it to None. 
            # Note: For sysadmin endpoints, we might not need a tenant.
            request.tenant = None

        response = self.get_response(request)
        return response
