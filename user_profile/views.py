from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from user_profile.models import UserProfile

from user_profile.utils.phone_authentication import authorise, verify_code


# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()

    def list(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

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


