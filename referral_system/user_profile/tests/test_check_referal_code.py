import pytest
from user_profile.models import UserProfile
from user_profile.utils.referral_code import check_referral_code

pytestmark = pytest.mark.django_db


from user_profile.tests.fixtures import create_user_profile


def test_valid_code_returns_profile(create_user_profile):
    """Если код существует — возвращается правильный профиль."""
    profile = create_user_profile(username="user1")
    profile.referral_number = "ABC123"
    profile.save()

    result = check_referral_code("ABC123")
    assert isinstance(result, UserProfile)
    assert result == profile


def test_invalid_code_raises_error():
    """Если кода нет — выбрасывается исключение UserProfile.DoesNotExist."""
    with pytest.raises(UserProfile.DoesNotExist):
        check_referral_code("INVALID")


def test_empty_code_raises_value_error():
    """Если код пустой — выбрасывается ValueError."""
    with pytest.raises(ValueError):
        check_referral_code("")


@pytest.mark.parametrize("code_variant", ["abc123", " AbC123 ", "ABC123"])
def test_code_is_case_insensitive(create_user_profile, code_variant):
    """Проверяем, что код можно вводить в любом регистре и с пробелами."""
    profile = create_user_profile(username="user2")
    profile.referral_number = "ABC123"
    profile.save()

    result = check_referral_code(code_variant)
    assert result == profile
