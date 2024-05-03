from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
@shared_task(bind=True)
def send_email_task(email_content, recipient):
    """Sends an email when the feedback form has been submitted."""
    # sleep(20)  # Simulate expensive operation(s) that freeze Django
    Message = f"\tmessage form Celery\n\nThank you!",
    MailSubject = 'Mail form Celery',
    ToEmail = 'ajayparihar876@gmail.com',
    import pdb;pdb.set_trace()
    send_mail(
        subject=MailSubject,
        message= Message,
        from_email= settings.EMAIL_HOST_USER,
        recipient_list=[ToEmail],
        fail_silently=False,
    )