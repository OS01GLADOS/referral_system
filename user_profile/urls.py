from rest_framework import routers

from user_profile.views import UserProfileViewSet

router = routers.DefaultRouter()

router.register(r'users', UserProfileViewSet)

