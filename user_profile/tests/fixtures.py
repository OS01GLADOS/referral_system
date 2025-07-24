import pytest
from django.contrib.auth import get_user_model

from user_profile.models import UserProfile


pytestmark = pytest.mark.django_db

User = get_user_model()

@pytest.fixture
def create_user_profile():
    def _create(phone="+79990000000", username="user1"):
        user = User.objects.create_user(username=username, password="password")
        profile = UserProfile.objects.create(user=user, phone_number=phone)
        return profile
    return _create
