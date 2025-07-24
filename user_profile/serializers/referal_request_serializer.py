from rest_framework import serializers


class ReferalRequestSerializer(serializers.Serializer):
    code = serializers.CharField()
