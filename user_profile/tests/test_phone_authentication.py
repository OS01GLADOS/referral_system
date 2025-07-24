import pytest
from django.contrib.auth import get_user_model
from user_profile.models import UserProfile
from user_profile.utils.phone_authentication import authorise

pytestmark = pytest.mark.django_db


User = get_user_model()


@pytest.fixture
def create_user():
    def _create_user(username="testuser", password="pass"):
        return User.objects.create_user(username=username, password=password)
    return _create_user


def test_authorise_returns_existing_user(create_user):
    """
    Если профиль уже существует, возвращается он же.
    """
    user = create_user()
    profile = UserProfile.objects.create(user=user, phone_number="+79990000000")

    result, _ = authorise("+79990000000")

    assert result.id == profile.id
    assert UserProfile.objects.count() == 1


def test_authorise_creates_new_user():
    """
    Если профиля нет, должен создаться новый профиль + новый пользователь.
    """
    result, _ = authorise("+79990000001")

    assert result.phone_number == "+79990000001"
    assert UserProfile.objects.count() == 1
    assert result.user is not None


def test_authorise_creates_different_users_for_different_numbers():
    """
    Для разных номеров должны создаваться разные профили и пользователи.
    """
    profile1, _ = authorise("+79990000001")
    profile2, _ = authorise("+79990000002")

    assert profile1.id != profile2.id
    assert profile1.user.id != profile2.user.id
    assert UserProfile.objects.count() == 2
