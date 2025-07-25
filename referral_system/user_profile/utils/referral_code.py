from user_profile.models import UserProfile


def check_referral_code(code: str) -> UserProfile:
    """
    Checks if the code is valid.
    returns profile, which code belongs to.

    :param code:
    :return: UserProfile
    """
    code = code.replace(' ', '')
    if code and code != "":
        return UserProfile.objects.get(referral_number__iexact=code)
    raise ValueError('code is empty')
