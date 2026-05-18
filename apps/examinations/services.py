from decimal import Decimal
from django.db.models import Sum, F
from apps.registration.models import Enrollment

class GPAService:
    @staticmethod
    def calculate_gpa(enrollment: Enrollment) -> Decimal:
        """
        Calculates the GPA for a specific enrollment (semester).
        GPA = sum(grade_points * credits) / total_credits
        Only includes courses that have a graded result.
        """
        graded_courses = enrollment.courses.filter(grade__isnull=False)
        
        if not graded_courses.exists():
            return Decimal('0.00')

        # Calculate sum of (grade_points * credits)
        total_points = graded_courses.aggregate(
            total=Sum(F('grade__grade_points') * F('course__credits'))
        )['total'] or Decimal('0.00')

        # Calculate total credits
        total_credits = graded_courses.aggregate(
            total=Sum('course__credits')
        )['total'] or 0

        if total_credits == 0:
            return Decimal('0.00')

        return round(total_points / Decimal(total_credits), 2)


class GradeScale:
    @staticmethod
    def from_score(score):
        score = Decimal(score)
        if score >= 90:
            return "A", Decimal("4.00")
        if score >= 80:
            return "B", Decimal("3.00")
        if score >= 70:
            return "C", Decimal("2.00")
        if score >= 60:
            return "D", Decimal("1.00")
        return "F", Decimal("0.00")
