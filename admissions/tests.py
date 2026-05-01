from django.test import TestCase
from tenants.models import University
from accounts.models import User
from .models import Application, Document


class ApplicationModelTest(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name="Adm Uni", slug="adm")

    def test_create_application(self):
        app = Application.objects.create(
            university=self.uni,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            program_applied="Computer Science",
            entry_year=2026,
        )
        self.assertEqual(app.status, 'pending')
        self.assertEqual(str(app), "John Doe - Computer Science")

    def test_application_status_transitions(self):
        app = Application.objects.create(
            university=self.uni,
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            program_applied="Engineering",
            entry_year=2026,
        )
        self.assertEqual(app.status, 'pending')
        app.status = 'accepted'
        app.save()
        app.refresh_from_db()
        self.assertEqual(app.status, 'accepted')

    def test_document_creation(self):
        app = Application.objects.create(
            university=self.uni,
            first_name="Bob",
            last_name="Brown",
            email="bob@example.com",
            program_applied="Medicine",
            entry_year=2026,
        )
        doc = Document.objects.create(
            university=self.uni,
            application=app,
            doc_type="Transcript",
            file="test.pdf",
        )
        self.assertFalse(doc.is_verified)
        doc.is_verified = True
        doc.save()
        doc.refresh_from_db()
        self.assertTrue(doc.is_verified)
