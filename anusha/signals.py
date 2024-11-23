# # signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import lapApplicationVerification

@receiver(post_save, sender=lapApplicationVerification)
def update_approved_timestamp(sender, instance, **kwargs):
    if instance.verification_status == 'Approved':
        instance.status_approved_at = timezone.now()
        instance.save()
        print(f"Signal triggered for ID {instance.id}, status_approved_at updated.")
