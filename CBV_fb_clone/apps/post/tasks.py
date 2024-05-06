from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from django.conf import settings

@shared_task()   
def send_email_task(*args, **kwargs):
    """Sends an email with the provided message."""
    plain_message = kwargs.get("plain_message")
    html_message = kwargs.get("html_message")
    mail_subject = 'Testing celery'
    to_email = 'Recipient Name <ajayparihar876@gmail.com>'  # Correct email format
    email = EmailMultiAlternatives(
        subject=mail_subject,
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
    
    return 'Email sent successfully'
