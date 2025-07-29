from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import requests
from django.core.files.base import ContentFile
from accounts.models import Profile

User = get_user_model()

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        email = sociallogin.user.email
        if not email:
            return

        try:
            existing_user = User.objects.get(email=email)
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user_profile = Profile.objects.get(user=user)
        data = sociallogin.account.extra_data

        first_name_from_provider = data.get('given_name') or data.get('first_name')
        last_name_from_provider = data.get('family_name') or data.get('last_name')

        if first_name_from_provider and not user_profile.first_name:
            user_profile.first_name = first_name_from_provider

        if last_name_from_provider and not user_profile.last_name:
            user_profile.last_name = last_name_from_provider

        picture_url = data.get('picture') or data.get('picture', {}).get('data', {}).get('url')

        if picture_url and not user_profile.profile_picture:
            response = requests.get(picture_url)
            if response.status_code == 200:
                filename = f'user_{user.id}_profile.jpg'
                user_profile.profile_picture.save(
                    filename,
                    ContentFile(response.content),
                    save=False
                )

        user_profile.save()
        return user