from rest_framework import routers

from user_profile.views import UserProfileViewSet, AuthRequestView

router = routers.DefaultRouter()

router.register(r'users', UserProfileViewSet)
router.register(r'authorisation', AuthRequestView, basename='authorisation')

