import pytest
from src.probability import weighted_random_choice
import random

# Фиксируем случайное число для повторяемости тестов
random.seed(42)

# Тестовые данные
TEST_ELEMENTS = ['a', 'b', 'c', 'd']
TEST_WEIGHTS = [1, 2, 3, 4]
TOTAL_WEIGHT = sum(TEST_WEIGHTS)

def test_basic_functionality():  # Проверка, что функция возвращает элемент из списка
    result = weighted_random_choice(TEST_ELEMENTS, TEST_WEIGHTS, x=0.1)
    assert result in TEST_ELEMENTS

def test_deterministic_choice():  # Проверка детерминированного выбора при заданном x
    assert weighted_random_choice(TEST_ELEMENTS, TEST_WEIGHTS, x=0.0) == 'a'

    assert weighted_random_choice(TEST_ELEMENTS, TEST_WEIGHTS, x=0.999) == 'd'

def test_probability_distribution():  # Проверка, что распределение вероятностей соответствует весам
    n_samples = 100000
    counts = {elem: 0 for elem in TEST_ELEMENTS}

    for _ in range(n_samples):
        elem = weighted_random_choice(TEST_ELEMENTS, TEST_WEIGHTS)
        counts[elem] += 1

    # Проверяем, что частота близка к ожидаемой вероятности (w_i / total_weight)
    for elem, weight in zip(TEST_ELEMENTS, TEST_WEIGHTS):
        expected_prob = weight / TOTAL_WEIGHT
        actual_prob = counts[elem] / n_samples
        assert pytest.approx(expected_prob, rel=0.05) == actual_prob

def test_empty_elements():  # Проверка ошибки при пустом списке элементов
    with pytest.raises(ValueError, match="Elements list cannot be empty"):
        weighted_random_choice([], [])

def test_mismatched_lengths():  # Проверка ошибки при разной длине elements и weights
    with pytest.raises(ValueError, match="must have the same length"):
        weighted_random_choice(['a', 'b'], [1])

def test_zero_weights():  # Проверка случая, когда все веса нулевые (должен вернуть случайный элемент)
    result = weighted_random_choice(['a', 'b', 'c'], [0, 0, 0])
    assert result in ['a', 'b', 'c']

def test_negative_weights():  # Проверка ошибки при отрицательных весах
    with pytest.raises(ValueError, match="Weights must be non-negative"):
        weighted_random_choice(['a', 'b'], [1, -1])

def test_x_out_of_range():  # Проверка ошибки, если x не в [0, 1]
    with pytest.raises(ValueError, match="x must be in \[0, 1\]"):
        weighted_random_choice(TEST_ELEMENTS, TEST_WEIGHTS, x=1.1)