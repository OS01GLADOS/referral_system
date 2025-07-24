from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from user_profile.models import UserProfile
from user_profile.serializers.user_profile_serializer import UserProfileSerializer
from user_profile.serializers.referal_request_serializer import ReferalRequestSerializer
from user_profile.serializers.authorization_serializer import AuthorizationSerializer

from user_profile.utils.phone_authentication import authorise, verify_code

from user_profile.utils.referal_code import check_referal_code


class AuthRequestView(viewsets.ViewSet):
    @extend_schema(
        operation_id="phone_authentication",
        summary="phone authentication",
        description="Returns all profiles",
        request=AuthorizationSerializer,
    )
    @action(detail=False, methods=["POST"])
    def phone(self, request):
        serializer = AuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone_number')
        code = serializer.validated_data.get('code')

        if code:
            profile = verify_code(phone, code)
            user = profile.user
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'token': str(refresh.access_token),
            })
        profile, sent_code = authorise(phone)
        return JsonResponse({
            'phone': phone,
            'code': sent_code,
        })


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    @extend_schema(
        operation_id="all_profiles",
        summary="all profiles",
        description="Returns all profiles",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="profile_detail",
        summary="profile detail",
        description="Returns profile detail by id",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="input_referal_code",
        summary="input referal code",
        description="Set referal code for currently logged in user",
        request=ReferalRequestSerializer,
    )
    @action(detail=False, methods=["POST"])
    def input_referal_code(self, request):
        code = request.data.get('code')
        try:
            check_referal_code(code)
        except Exception as e:
            return JsonResponse({'error':'Invalid referal code'},status=400)



        # for authenticated user only
        # can activate only one code, else - error
        raise NotImplementedError("Логика проверки кода ещё не реализована")


