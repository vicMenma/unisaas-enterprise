import io
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from registration.models import EnrollmentCourse
from examinations.models import Grade


class TranscriptService:
    """Generates an official academic transcript PDF for a student."""

    @staticmethod
    def generate_transcript(student):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # --- Header ---
        p.setFont("Helvetica-Bold", 22)
        p.drawCentredString(width / 2, height - 0.8 * inch, student.university.name)
        p.setFont("Helvetica", 11)
        p.drawCentredString(width / 2, height - 1.05 * inch, "OFFICIAL ACADEMIC TRANSCRIPT")

        # --- Student Info ---
        y = height - 1.6 * inch
        p.setFont("Helvetica-Bold", 10)
        p.drawString(1 * inch, y, f"Student: {student.user.email}")
        p.drawString(4 * inch, y, f"Matricule: {student.matricule}")
        y -= 0.2 * inch
        p.drawString(1 * inch, y, f"Program: {student.program_id}")
        p.drawString(4 * inch, y, f"Entry Year: {student.entry_year}")

        # --- Table Header ---
        y -= 0.5 * inch
        p.setFont("Helvetica-Bold", 9)
        for label, x in [("Code", 1), ("Course", 2), ("Credits", 4), ("Grade", 5), ("Points", 5.8)]:
            p.drawString(x * inch, y, label)
        y -= 0.15 * inch
        p.line(1 * inch, y, 6.5 * inch, y)
        y -= 0.2 * inch

        # --- Rows ---
        p.setFont("Helvetica", 9)
        total_points = Decimal("0")
        total_credits = 0
        enrollments = student.enrollments.all()
        for enrollment in enrollments:
            for ec in enrollment.courses.all():
                grade = getattr(ec, 'grade', None)
                if grade is None:
                    continue
                p.drawString(1 * inch, y, ec.course.code)
                p.drawString(2 * inch, y, ec.course.name[:30])
                p.drawString(4 * inch, y, str(ec.course.credits))
                p.drawString(5 * inch, y, grade.letter_grade)
                p.drawString(5.8 * inch, y, str(grade.grade_points))
                total_points += grade.grade_points * ec.course.credits
                total_credits += ec.course.credits
                y -= 0.2 * inch
                if y < 1.5 * inch:
                    p.showPage()
                    y = height - 1 * inch

        # --- GPA Summary ---
        y -= 0.3 * inch
        p.line(1 * inch, y, 6.5 * inch, y)
        y -= 0.25 * inch
        gpa = round(total_points / Decimal(total_credits), 2) if total_credits else Decimal("0.00")
        p.setFont("Helvetica-Bold", 11)
        p.drawString(1 * inch, y, f"Cumulative GPA: {gpa}")
        p.drawString(4 * inch, y, f"Total Credits: {total_credits}")

        # --- Footer ---
        p.setFont("Helvetica-Oblique", 7)
        p.drawCentredString(
            width / 2, 0.5 * inch,
            f"Electronically generated — University ID: {student.university.id}",
        )

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
