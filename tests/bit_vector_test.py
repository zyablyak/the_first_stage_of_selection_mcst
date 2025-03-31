import pytest
from src.bit_vector import BitVector


class TestBitVectorInitialization:
    def test_empty_initialization(self):
        bv = BitVector(8)
        assert bv.bit_length() == 8
        assert bv.to_hex_string() == '00'

    def test_data_initialization(self):
        bv = BitVector(16, [0xABCD])
        assert bv.to_hex_string() == 'cdab'

        bv = BitVector(64, [0x0123456789ABCDEF])
        assert bv.to_hex_string() == 'efcdab8967452301'

        bv = BitVector(12, [0xFFF])
        assert bv.to_hex_string() == 'ff0f'

    def test_invalid_initialization(self):
        with pytest.raises(ValueError):
            BitVector(0)  # Нулевая длина

        with pytest.raises(ValueError):
            BitVector(64, [])  # Недостаточно данных


class TestBitOperations:
    def test_bit_access(self):
        bv = BitVector(16, [0xAAAA])

        # Проверка установленных битов (0xAAAA = 1010101010101010)
        for i in range(16):
            assert bv._get_bit(i) == (i % 2 == 1), f"Bit {i} should be {i % 2 == 1}"

        # Проверка верхней границы
        with pytest.raises(IndexError, match=r"Bit position 16 out of range \(0\.\.15\)"):
            bv._get_bit(16)

        # Проверка нижней границы (отрицательные индексы)
        with pytest.raises(IndexError, match=r"Bit position -1 out of range \(0\.\.15\)"):
            bv._get_bit(-1)

        # Проверка сообщения об ошибке
        try:
            bv._get_bit(20)
            pytest.fail("Should have raised IndexError")
        except IndexError as e:
            assert "Bit position 20 out of range (0..15)" in str(e)

    def test_bit_manipulation(self):
        bv = BitVector(8)

        # Установка и сброс битов
        for i in range(8):
            bv._set_bit(i, True)
            assert bv._get_bit(i) is True
            bv._set_bit(i, False)
            assert bv._get_bit(i) is False


class TestBitfieldOperations:
    def test_set_bitfield_from_vector(self):
        src = BitVector(8, [0xFF])
        dst = BitVector(16)

        dst.set_bitfield(4, src)
        assert dst.get_bitfield_as_int(4, 8) == 0xFF
        assert dst.to_hex_string() == 'f00f'

    def test_set_bitfield_from_int(self):
        bv = BitVector(32)

        bv.set_bitfield(8, 0xABCD, 16)
        assert bv.get_bitfield_as_int(8, 16) == 0xABCD
        assert bv.to_hex_string() == '00cdab00'

    def test_clear_bitfield(self):
        bv = BitVector(16, [0xFFFF])

        bv.set_bitfield(4, None, 8)
        assert bv.get_bitfield_as_int(0, 16) == 0xF00F

    def test_get_bitfield(self):
        bv = BitVector(64, [0x0123456789ABCDEF])

        # Получение битового поля (биты 8-23)
        field = bv.get_bitfield(8, 16)
        assert isinstance(field, BitVector)
        assert field.bit_length() == 16

        # Проверяем hex-представление
        assert field.to_hex_string() == 'cdab'

        # Проверяем числовое значение
        assert field.get_bitfield_as_int(0, 16) == 0xABCD

        # Проверяем другое поле (биты 32-47)
        assert bv.get_bitfield_as_int(32, 16) == 0x4567

    def test_bitfield_edge_cases(self):
        bv = BitVector(128)

        # Граничные случаи
        with pytest.raises(ValueError):
            bv.set_bitfield(120, 0xFF, 16)  # Выход за границы

        with pytest.raises(ValueError):
            bv.get_bitfield(120, 16)  # Выход за границы

        with pytest.raises(TypeError):
            bv.set_bitfield(0, "invalid")  # Неверный тип


class TestHexRepresentation:
    def test_hex_output(self):
        bv = BitVector(24, [0x123456])
        assert str(bv) == '563412'
        assert repr(bv) == "BitVector(24, '563412')"

        # Частичный байт
        bv = BitVector(12, [0xFFF])
        assert bv.to_hex_string() == 'ff0f'


class TestLargeBitVectors:
    def test_large_vector(self):
        size = 1024
        bv = BitVector(size)

        # Установка и проверка битового поля
        bv.set_bitfield(100, 0xFFFFFFFF, 32)
        assert bv.get_bitfield_as_int(100, 32) == 0xFFFFFFFF

        # Проверка границ
        with pytest.raises(ValueError):
            bv.set_bitfield(size - 31, 0xFFFFFFFF, 32)


class TestSpecialCases:
    def test_single_bit_operations(self):
        bv = BitVector(1)

        bv._set_bit(0, True)
        assert bv._get_bit(0) is True
        assert bv.to_hex_string() == '01'

        bv._set_bit(0, False)
        assert bv._get_bit(0) is False
        assert bv.to_hex_string() == '00'

    def test_odd_bit_length(self):
        bv = BitVector(7, [0xFF])
        assert bv.to_hex_string() == '7f'  # Только 7 бит