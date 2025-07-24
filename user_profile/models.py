from django.db import models
from django.conf import settings
from core.code_generator import generate


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, unique=True)

    referal_number = models.CharField(max_length=6, unique=True, null=True, blank=True)
    parent_referal = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user} {self.phone_number}"

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        if not self.referal_number:
            self.referal_number = generate(settings.USER_PROFILE_REF_CODE_LENGTH)
