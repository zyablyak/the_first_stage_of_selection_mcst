from typing import Union, List


class BitVector:
    def __init__(self, bit_length: int, data: List[int] = None) -> None: # Инициализация битового вектора
        if bit_length <= 0:
            raise ValueError("Bit length must be positive")

        # Основные свойства вектора
        self._bit_length = bit_length  # Общее количество битов
        self._byte_length = (bit_length + 7) // 8  # Количество необходимых байтов
        self._data = bytearray(self._byte_length)  # Хранилище данных

        if data is not None:
            # Проверка достаточности данных
            if len(data) * 64 < bit_length:
                raise ValueError("Insufficient data for specified bit length")

            # Заполнение вектора битами из входных данных
            bit_pos = 0
            for num in data:
                for j in range(64):  # Обрабатываем все 64 бита каждого числа
                    if bit_pos >= bit_length:
                        break
                    if num & (1 << j):  # Проверка j-го бита числа
                        self._set_bit(bit_pos, True)
                    bit_pos += 1

    def __str__(self) -> str:  # Строковое представление в виде hex-строки
        return self.to_hex_string()

    def __repr__(self) -> str:  # Формальное строковое представление
        return f"BitVector({self._bit_length}, '{self.to_hex_string()}')"

    def bit_length(self) -> int:  # Возвращает общее количество битов в векторе
        return self._bit_length

    def set_bitfield(self, offset: int, bitfield: Union['BitVector', int, None], bitfield_length: int = None) -> None:  # Установка битового поля в векторе
        if isinstance(bitfield, BitVector):
            # Установка из другого BitVector
            if offset + bitfield.bit_length() > self._bit_length:
                raise ValueError("Bitfield out of range")
            for i in range(bitfield.bit_length()):
                self._set_bit(offset + i, bitfield._get_bit(i))
        elif isinstance(bitfield, int):
            # Установка из целого числа (до 64 бит)
            if bitfield_length is None:
                raise ValueError("bitfield_length required for integer bitfield")
            if bitfield_length > 64:
                raise ValueError("Integer bitfield limited to 64 bits")
            if offset + bitfield_length > self._bit_length:
                raise ValueError("Bitfield out of range")
            for i in range(bitfield_length):
                self._set_bit(offset + i, bool(bitfield & (1 << i)))
        elif bitfield is None:
            # Очистка битового поля
            if bitfield_length is None:
                raise ValueError("bitfield_length required for None bitfield")
            if offset + bitfield_length > self._bit_length:
                raise ValueError("Bitfield out of range")
            for i in range(bitfield_length):
                self._set_bit(offset + i, False)
        else:
            raise TypeError("Unsupported bitfield type")

    def get_bitfield(self, offset: int, length: int) -> 'BitVector':  # Извлечение битового поля как нового BitVector
        if offset + length > self._bit_length:
            raise ValueError("Bitfield out of range")

        result = BitVector(length)
        for i in range(length):
            result._set_bit(i, self._get_bit(offset + i))
        return result

    def get_bitfield_as_int(self, offset: int, length: int) -> int:  # Извлечение битового поля как целого числа
        if length > 64:
            raise ValueError("Integer bitfield limited to 64 bits")
        if offset + length > self._bit_length:
            raise ValueError("Bitfield out of range")

        result = 0
        for i in range(length):
            if self._get_bit(offset + i):
                result |= (1 << i)  # Устанавливаем i-й бит результата
        return result

    def to_hex_string(self) -> str:  # Возвращает hex-представление вектора
        return self._data.hex()

    def _get_bit(self, pos: int) -> bool:  # Внутренний метод для чтения бита по позиции
        if pos < 0 or pos >= self._bit_length:
            raise IndexError(f"Bit position {pos} out of range (0..{self._bit_length - 1})")
        byte_pos = pos // 8
        bit_pos = pos % 8
        return bool(self._data[byte_pos] & (1 << bit_pos))

    def _set_bit(self, pos: int, value: bool) -> None:  # Внутренний метод для установки бита по позиции
        if pos < 0 or pos >= self._bit_length:
            raise IndexError(f"Bit position {pos} out of range (0..{self._bit_length - 1})")
        byte_pos = pos // 8
        bit_pos = pos % 8
        if value:
            self._data[byte_pos] |= (1 << bit_pos)  # Установка бита
        else:
            self._data[byte_pos] &= ~(1 << bit_pos)  # Сброс бита