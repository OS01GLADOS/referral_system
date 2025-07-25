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

    child_referrals = serializers.SerializerMethodField()

    def get_child_referrals(self, obj) -> ChildUserProfileSerializer(many=True):
        children = UserProfile.objects.filter(parent_referral=obj)
        return ChildUserProfileSerializer(children, many=True).data

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'phone_number',
            'referral_number',
            'child_referrals',
        ]


class ParentReferalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['parent_referral']

    def validate(self, attrs):
        """
        Общая валидация: проверяем, можно ли назначить родителя
        """
        code_profile = self.context['profile']

        if self.instance.parent_referral:
            raise ValidationError(
                {"parent_referral": "You have already activated referal code"}
            )

        if code_profile == self.instance:
            raise ValidationError(
                {"parent_referral": "You can't activate yours referal code"}
            )
        attrs['parent_referral'] = code_profile
        return attrs

    def update(self, instance, validated_data):
        instance.parent_referral = validated_data['parent_referral']
        instance.save()
        return instance
