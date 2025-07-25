from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from user_profile.models import UserProfile
from user_profile.serializers.user_profile_serializer import UserProfileSerializer, ParentReferalSerializer
from user_profile.serializers.referral_request_serializer import ReferralRequestSerializer
from user_profile.serializers.authorization_serializer import AuthorizationSerializer, AuthorizationReqestSerializer, TokenSerializer

from user_profile.utils.phone_authentication import authorise, verify_code

class AuthRequestView(viewsets.ViewSet):
    @extend_schema(
        operation_id="phone_authentication",
        summary="phone authentication",
        description="Allows authentication with phone number",
        request=AuthorizationReqestSerializer,
        responses={
            200: OpenApiResponse(
                response=AuthorizationSerializer,
                description="user was created, confirmation code was sent"

            )
        },
    )
    @action(detail=False, methods=["POST"])
    def phone(self, request):
        serializer = AuthorizationReqestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone_number')
        profile, sent_code = authorise(phone)
        return JsonResponse({
            'phone_number': phone,
            'code': sent_code,
        })

    @extend_schema(
        operation_id="phone_authentication_confirm",
        summary="phone authentication confirmation",
        description="Confirms authentication with phone number",
        request=AuthorizationSerializer,
        responses={
            200: OpenApiResponse(
                response=TokenSerializer,
                description="phone confirmed successfully"
            ),
        },
    )
    @action(detail=False, methods=["POST"])
    def phone_confirm(self, request):
        serializer = AuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone_number')
        code = serializer.validated_data.get('code')
        profile = verify_code(phone, code)
        user = profile.user
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'token': str(refresh.access_token),
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
        request=ReferralRequestSerializer,
    )
    @action(detail=False, methods=["POST"])
    def input_referral_code(self, request):
        serializer = ReferralRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code_profile = serializer.context['profile']
        current_user_profile = UserProfile.objects.get(user=request.user)

        serializer = ParentReferalSerializer(
            instance=current_user_profile,
            data={},
            context={'profile': code_profile}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(UserProfileSerializer(current_user_profile).data)

