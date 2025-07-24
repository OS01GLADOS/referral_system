from rest_framework import serializers
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

    def get_child_referals(self, obj):
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
