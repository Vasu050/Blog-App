from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def assign_username(sender, instance, created, **kwargs):
    if created and not instance.username:
        # Automatically assign a username if it is not set
        instance.username = instance.email.split('@')[0]  # Use the email prefix as the username
        instance.save()
