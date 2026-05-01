from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email_task(user_id):
    """
    Simulates an idempotent background task to send an email to a new student.
    """
    logger.info(f"Sending welcome email to user {user_id}...")
    # In a real system, send email via Django's send_mail here
    return f"Email sent to {user_id}"
