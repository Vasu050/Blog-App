from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth.models import User
from allauth.account.adapter import DefaultAccountAdapter

# Custom adapter for handling Google login and user linking
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Extract email from Google data
        email = sociallogin.account.extra_data.get('email')

        if email:
            try:
                # Check if user already exists with the same email
                existing_user = User.objects.get(email=email)
                sociallogin.user = existing_user  # Link existing user to the social login
            except User.DoesNotExist:
                # If user doesn't exist, let Allauth create a new user
                user = sociallogin.user
                
                user.username = email.split('@')[0]
                user.set_password(f"{user.username}123")  # Set a default password
                user.save()

        return super().pre_social_login(request, sociallogin)


