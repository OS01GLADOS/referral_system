import pytest
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from user_profile.models import UserProfile
from user_profile.utils.phone_authentication import verify_code

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture
def create_user_profile():
    def _create(phone="+79990000000", username="user1"):
        user = User.objects.create_user(username=username, password="password")
        profile = UserProfile.objects.create(user=user, phone_number=phone)
        return profile
    return _create


def test_verify_code_success(create_user_profile):
    profile = create_user_profile()

    # Сохраняем правильный код в кеш
    cache.set(f"auth_code:{profile.phone_number}", "123456", timeout=300)

    # Проверяем, что функция возвращает профиль
    result = verify_code(profile.phone_number, "123456")
    assert result == profile


def test_verify_code_wrong_code(create_user_profile):
    profile = create_user_profile()
    cache.set(f"auth_code:{profile.phone_number}", "123456", timeout=300)

    with pytest.raises(ValidationError):
        verify_code(profile.phone_number, "000000")


def test_verify_code_no_code_in_cache(create_user_profile):
    profile = create_user_profile()
    cache.delete(f"auth_code:{profile.phone_number}")  # Явно очищаем

    with pytest.raises(ValidationError):
        verify_code(profile.phone_number, "123456")


def test_verify_code_no_user_for_phone():
    # Сохраним код в кеше, но пользователя с таким номером нет
    phone = "+79991112233"
    cache.set(f"auth_code:{phone}", "123456", timeout=300)

    with pytest.raises(UserProfile.DoesNotExist):
        verify_code(phone, "123456")