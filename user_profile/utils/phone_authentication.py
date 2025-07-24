import time

from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from user_profile.models import UserProfile
from core.code_generator import generate


User = get_user_model()


def send_phone_confirmation(phone_number):
    # sleep for 2 sec
    time.sleep(2)
    return generate(settings.USER_PROFILE_PHONE_CONFIRMATION_CODE_LENGTH)


def authorise(phone_number: str) -> tuple[UserProfile, str]:
    """
    authorises a phone number and creates user if not exists

    :param phone_number:
    :return: UserProfile, code (as it now used for testing)
    """
    code = send_phone_confirmation(phone_number)
    cache.set(f"phone_confirm:{phone_number}", code, timeout=300)

    requested_profile = UserProfile.objects.filter(phone_number=phone_number).first()
    if requested_profile:
        return requested_profile, code

    user = User.objects.create_user(
        username=phone_number,
        password=None
    )

    profile = UserProfile.objects.create(
        user=user,
        phone_number=phone_number
    )

    return profile, code


def verify_code(phone: str, code: str) -> UserProfile:
    """
    verifies the phone code

    :param phone:
    :param code:
    :return: UserProfile
    """
    cached_code = cache.get(f"phone_confirm:{phone}")

    if not cached_code or cached_code != code:
        raise ValidationError("Code doesn't match")

    return UserProfile.objects.get(phone_number=phone)
