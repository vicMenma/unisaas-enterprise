import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors

class AdmissionDocumentService:
    @staticmethod
    def generate_offer_letter(application):
        """
        Generates a professional PDF offer letter for an accepted application.
        """
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Header
        p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(width/2, height - 1*inch, application.university.name)
        
        p.setFont("Helvetica", 12)
        p.drawCentredString(width/2, height - 1.3*inch, "Official Letter of Admission")
        
        # Date & Reference
        p.setFont("Helvetica", 10)
        p.drawString(1*inch, height - 2*inch, f"Date: {application.submission_date.strftime('%d %B %Y')}")
        p.drawString(1*inch, height - 2.2*inch, f"Ref: ADM-{application.id}")

        # Recipient
        p.setFont("Helvetica-Bold", 12)
        p.drawString(1*inch, height - 3*inch, f"To: {application.first_name} {application.last_name}")
        p.setFont("Helvetica", 10)
        p.drawString(1*inch, height - 3.2*inch, application.email)

        # Body
        p.setFont("Helvetica", 12)
        text = f"Dear {application.first_name},"
        p.drawString(1*inch, height - 4*inch, text)
        
        body = [
            f"We are pleased to inform you that your application for the {application.program_applied}",
            f"program at {application.university.name} has been successful.",
            "",
            "This offer is subject to the verification of your original documents and the",
            "payment of the initial registration fees.",
            "",
            "Welcome to our academic community!"
        ]
        
        y = height - 4.5*inch
        for line in body:
            p.drawString(1*inch, y, line)
            y -= 0.2*inch

        # Footer / Signature
        p.line(1*inch, 2*inch, 3*inch, 2*inch)
        p.drawString(1*inch, 1.8*inch, "Registrar of Admissions")
        
        p.setFont("Helvetica-Oblique", 8)
        p.drawCentredString(width/2, 0.5*inch, f"This is an electronically generated document. University ID: {application.university.id}")

        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer
