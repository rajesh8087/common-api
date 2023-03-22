from django.db.models.signals import post_save
from django.dispatch import receiver
from api import settings
from django.core.mail import EmailMessage, send_mail


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        subject = "User Credentials"
        message = f"Dear {instance.name},\n\nThank you for registering on our website.Here are your login credentials, username - {instance.email}."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()
