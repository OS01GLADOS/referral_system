import string
import random


def generate(length: int) -> str:
    """
    generate code of required length with numbers and symbols

    :param length:
    :return: generated code
    """
    if length < 0:
        raise ValueError("length is less than 0")
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))
