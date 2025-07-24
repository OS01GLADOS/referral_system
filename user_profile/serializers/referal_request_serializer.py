from rest_framework import serializers

from user_profile.models import UserProfile

from user_profile.utils.referal_code import check_referal_code


class ReferalRequestSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        try:
            profile = check_referal_code(value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Неверный реферальный код")
        except ValueError:
            raise serializers.ValidationError("Код не может быть пустым")

        # можно вернуть профиль для дальнейшего использования
        self.context['profile'] = profile
        return value
