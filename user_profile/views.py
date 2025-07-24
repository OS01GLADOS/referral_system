from django.http import JsonResponse
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from user_profile.models import UserProfile
from user_profile.serializers.UserProfileSerializer import UserProfileSerializer

from user_profile.utils.phone_authentication import authorise, verify_code


# Create your views here.
class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @extend_schema(
        operation_id="all_profiles",   # заменяет название метода
        summary="all profiles",         # заголовок в ReDoc
        description="Returns all profiles",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="profile_detail",
        summary="Profile detail",
        description="Returns profile detail by id",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # auth with phone number
    def auth_request(self, request):
        request_json = {}
        phone = request_json.get('phone_number')
        code = request_json.get('code', None)
        if code:
            profile = verify_code(phone, code)  # возвращает UserProfile или выбрасывает ValidationError
            user = profile.user
            raise NotImplementedError("Логика проверки кода ещё не реализована")
            # return get auth token
        profile, sent_code = authorise(phone)
        return JsonResponse({
            'phone': phone,
            'code': sent_code,
        })


    # input referal number
    def input_referal_code(self, request):
        # for authenticated user only
        # can activate only one code, else - error
        pass


