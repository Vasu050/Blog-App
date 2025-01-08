from django.db import models
from django.contrib.auth.models import User
'''from django.utils import timezone
import random
import string
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import AbstractUser'''

# Create your models here.
'''
class PasswordResetRequest(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=32, default=get_random_string(32), editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    # Define token validity period (e.g., 1 hour)
    TOKEN_VALIDITY_PERIOD = timezone.timedelta(hours=1)

    def generate_token(self):
        """Generate a random 32-character token"""
        self.token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def is_valid(self):
        """Check if the reset request is still valid (e.g., within 1 hour)"""
        expiration_time = timezone.now() - timezone.timedelta(hours=1)
        return self.created_at > expiration_time and not self.is_used

    def send_reset_email(self):
        """Send reset email to the user"""
        reset_url = f"http://yourdomain.com/reset-password/{self.token}/"
        # Use Django's send_mail function or any other method to send the reset URL
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_url}',
            'from@example.com',
            [self.email],
            fail_silently=False,
        )'''