# работает за O(1)
def is_pow_of_two(a: int) -> bool:
    if a <= 0:
        return False
    return (a & (a - 1)) == 0

