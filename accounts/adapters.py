from io import BytesIO

import requests
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from PIL import Image

from accounts.models import Profile

UserModel = get_user_model()


def get_profile_picture_url(provider_data):
    picture = provider_data.get("picture")


    if isinstance(picture, dict):
        picture_data = picture.get("data")

        if not isinstance(picture_data, dict):
            return None

        picture = picture_data.get("url")


    if isinstance(picture, str):
        return picture.strip() or None

    return None


def save_profile_picture(profile, picture_url):
    if profile.profile_picture or not picture_url:
        return

    try:
        with requests.get(picture_url, timeout=5) as response:
            response.raise_for_status()
            image_content = response.content


        with Image.open(BytesIO(image_content)) as picture:
            image_format = picture.format
            picture.verify()

    except (requests.RequestException, OSError, ValueError):
        return

    extension = {
        "JPEG": "jpg",
        "PNG": "png",
        "WEBP": "webp",
        "GIF": "gif",
    }.get(image_format)

    if not extension:
        return

    profile.profile_picture.save(
        f"user_{profile.user_id}_profile.{extension}",
        ContentFile(image_content),
        save=False,
    )


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        email = sociallogin.user.email
        if not email:
            return

        try:
            existing_user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return

        sociallogin.connect(request, existing_user)

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        profile = Profile.objects.get(user=user)
        provider_data = sociallogin.account.extra_data

        first_name = provider_data.get("given_name") or provider_data.get("first_name")
        last_name = provider_data.get("family_name") or provider_data.get("last_name")

        if first_name and not profile.first_name:
            profile.first_name = first_name

        if last_name and not profile.last_name:
            profile.last_name = last_name

        picture_url = get_profile_picture_url(provider_data)
        save_profile_picture(profile, picture_url)

        profile.save()
        return user
