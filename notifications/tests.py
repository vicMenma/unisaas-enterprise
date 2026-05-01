from django.test import TestCase
from tenants.models import University
from accounts.models import User
from .models import Notification


class NotificationModelTest(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name="Notif Uni", slug="notif")
        self.user = User.objects.create_user(
            email="user@notif.com", university=self.uni, password="pass",
        )

    def test_notification_defaults(self):
        n = Notification.objects.create(
            university=self.uni, recipient=self.user,
            title="Welcome", message="Welcome to the university!",
        )
        self.assertFalse(n.is_read)
        self.assertEqual(n.channel, 'in_app')
        self.assertEqual(n.priority, 'normal')
        self.assertIsNone(n.read_at)
