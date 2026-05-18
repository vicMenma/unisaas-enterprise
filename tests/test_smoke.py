from django.test import TestCase, override_settings


class SmokePageTest(TestCase):
    def test_frontend_pages_render(self):
        for path in ["/", "/login/", "/portal/", "/dean-portal/"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)

    def test_api_root_requires_authentication(self):
        response = self.client.get("/api/v1/")
        self.assertEqual(response.status_code, 401)

    @override_settings(ALLOWED_HOSTS=["unisaas-enterprise.onrender.com"], TENANT_PARENT_DOMAINS=[])
    def test_platform_host_does_not_become_tenant_slug(self):
        response = self.client.get("/", HTTP_HOST="unisaas-enterprise.onrender.com")
        self.assertEqual(response.status_code, 200)

    @override_settings(ALLOWED_HOSTS=["missing.example.edu"], TENANT_PARENT_DOMAINS=["example.edu"])
    def test_configured_tenant_subdomains_are_validated(self):
        response = self.client.get("/", HTTP_HOST="missing.example.edu")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid tenant specified")
