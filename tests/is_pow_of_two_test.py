import pytest
from src.is_pow_of_two import is_pow_of_two

# Позитивные тесты: числа, которые являются степенями двойки
@pytest.mark.parametrize("num", [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
def test_is_power_of_two_true(num):
    assert is_pow_of_two(num) is True

# Негативные тесты: числа, которые НЕ являются степенями двойки
@pytest.mark.parametrize("num", [3, 5, 6, 7, 9, 10, 15, 17, 31, 33, 127, 129])
def test_is_power_of_two_false(num):
    assert is_pow_of_two(num) is False

# Граничные случаи: ноль и отрицательные числа
@pytest.mark.parametrize("num", [0, -1, -2, -4, -8, -16])
def test_non_positive_numbers(num):
    assert is_pow_of_two(num) is False

# Большие числа (проверка на переполнение)
@pytest.mark.parametrize("num", [2**30, 2**50, 2**100])
def test_large_powers_of_two(num):
    assert is_pow_of_two(num) is True

# Большие числа, не являющиеся степенями двойки
@pytest.mark.parametrize("num", [2**30 + 1, 2**50 - 1, 2**100 + 5])
def test_large_non_powers_of_two(num):
    assert is_pow_of_two(num) is False