from rest_framework import serializers


class AuthorizationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField( required=False) # allow it to be null
