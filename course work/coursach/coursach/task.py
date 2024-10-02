from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_daily_email():
    
    subject = 'Ежедневное уведомление'
    message = 'Это ваше ежедневное уведомление о днях рождениях или акциях.'
    
    send_mail(
        subject,
        message,
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )