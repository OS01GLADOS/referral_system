import pytest

from core.code_generator import generate


def test_generate_returns_string():
    result = generate(5)
    assert isinstance(result, str)


@pytest.mark.parametrize("length", [0, 1, 5, 10, 50])
def test_generate_length(length):
    result = generate(length)
    assert len(result) == length


def test_generate_different_results():
    # Проверяем, что хотя бы иногда результаты разные
    result1 = generate(10)
    result2 = generate(10)
    assert result1 != result2


def test_generate_only_digits_and_symbols():
    # Предположим, что символы — это цифры и латинские буквы (уточни, если нужно другое)
    allowed_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = generate(20)
    assert all(ch in allowed_chars for ch in result)


def test_generate_negative_length():
    # Ожидаем, что при отрицательной длине будет исключение (или уточни поведение)
    with pytest.raises(ValueError):
        generate(-5)