from django.db.models import Sum, Count
from students.models import StudentProfile
from finance.models import Invoice, Payment
from admissions.models import Application

class UniversityReportService:
    """
    Business Intelligence (BI) service for university leadership.
    """
    @staticmethod
    def get_financial_summary(university):
        data = Invoice.objects.filter(university=university).aggregate(
            total_invoiced=Sum('total_amount'),
            total_collected=Sum('paid_amount')
        )
        return {
            "invoiced": data['total_invoiced'] or 0,
            "collected": data['total_collected'] or 0,
            "pending": (data['total_invoiced'] or 0) - (data['total_collected'] or 0)
        }

    @staticmethod
    def get_enrollment_stats(university):
        return {
            "total_students": StudentProfile.objects.filter(university=university).count(),
            "new_applications": Application.objects.filter(university=university, status='pending').count()
        }
