from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class AuthorizationReqestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class AuthorizationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()
