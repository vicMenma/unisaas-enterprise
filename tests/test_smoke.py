from django.test import TestCase


class SmokePageTest(TestCase):
    def test_frontend_pages_render(self):
        for path in ["/", "/login/", "/portal/", "/dean-portal/"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)

    def test_api_root_requires_authentication(self):
        response = self.client.get("/api/v1/")
        self.assertEqual(response.status_code, 401)
