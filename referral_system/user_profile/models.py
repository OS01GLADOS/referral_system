from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from core.code_generator import generate

User = get_user_model()


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, unique=True)

    referral_number = models.CharField(max_length=6, null=True, blank=True)
    parent_referral = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user} {self.phone_number} {self.referral_number}"

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        if not self.referral_number:
            self.referral_number = generate(settings.USER_PROFILE_REF_CODE_LENGTH)
