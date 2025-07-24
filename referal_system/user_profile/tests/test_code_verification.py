import pytest
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from user_profile.models import UserProfile
from user_profile.utils.phone_authentication import verify_code

from user_profile.tests.fixtures import create_user_profile

pytestmark = pytest.mark.django_db


def test_verify_code_success(create_user_profile):
    profile = create_user_profile()

    # Сохраняем правильный код в кеш
    cache.set(f"phone_confirm:{profile.phone_number}", "123456", timeout=300)

    # Проверяем, что функция возвращает профиль
    result = verify_code(profile.phone_number, "123456")
    assert result == profile


def test_verify_code_wrong_code(create_user_profile):
    profile = create_user_profile()
    cache.set(f"phone_confirm:{profile.phone_number}", "123456", timeout=300)

    with pytest.raises(ValidationError):
        verify_code(profile.phone_number, "000000")


def test_verify_code_no_code_in_cache(create_user_profile):
    profile = create_user_profile()
    cache.delete(f"phone_confirm:{profile.phone_number}")  # Явно очищаем

    with pytest.raises(ValidationError):
        verify_code(profile.phone_number, "123456")


def test_verify_code_no_user_for_phone():
    # Сохраним код в кеше, но пользователя с таким номером нет
    phone = "+79991112233"
    cache.set(f"phone_confirm:{phone}", "123456", timeout=300)

    with pytest.raises(UserProfile.DoesNotExist):
        verify_code(phone, "123456")
