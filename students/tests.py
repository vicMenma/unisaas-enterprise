from django.test import TestCase
from tenants.models import University
from accounts.models import User
from .models import StudentProfile, MatriculeSequence
from .services import MatriculeService

class MatriculeServiceTest(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name="Test Uni", slug="test")
        
    def test_matricule_generation_is_sequential(self):
        """
        Verify that matricules are generated sequentially and correctly formatted.
        """
        m1 = MatriculeService.generate_matricule(self.uni, 2026, "CS", 1)
        m2 = MatriculeService.generate_matricule(self.uni, 2026, "CS", 1)
        
        self.assertEqual(m1, "TEST-2026-CS-1-0001")
        self.assertEqual(m2, "TEST-2026-CS-1-0002")
        
        seq = MatriculeSequence.objects.get(university=self.uni, year=2026, program_code="CS", level=1)
        self.assertEqual(seq.current_sequence, 2)

    def test_matricule_format(self):
        """
        Verify the format structure: SLUG-YEAR-PROG-LEVEL-SEQ
        """
        matricule = MatriculeService.generate_matricule(self.uni, 2026, "MED", 4)
        self.assertEqual(matricule, "TEST-2026-MED-4-0001")
