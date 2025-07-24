from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user_profile.models import UserProfile


class ChildUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'phone_number',
        ]


class UserProfileSerializer(serializers.ModelSerializer):

    child_referals = serializers.SerializerMethodField()

    def get_child_referals(self, obj) -> ChildUserProfileSerializer(many=True):
        children = UserProfile.objects.filter(parent_referal=obj)
        return ChildUserProfileSerializer(children, many=True).data

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'phone_number',
            'referal_number',
            'child_referals',
        ]


class ParentReferalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['parent_referal']

    def validate(self, attrs):
        """
        Общая валидация: проверяем, можно ли назначить родителя
        """
        code_profile = self.context['profile']

        if self.instance.parent_referal:
            raise ValidationError(
                {"parent_referal": "You have already activated referal code"}
            )

        if code_profile == self.instance:
            raise ValidationError(
                {"parent_referal": "You can't activate yours referal code"}
            )
        attrs['parent_referal'] = code_profile
        return attrs

    def update(self, instance, validated_data):
        instance.parent_referal = validated_data['parent_referal']
        instance.save()
        return instance
