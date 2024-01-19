from functools import cache
@cache
def F(n: int) -> int:
    if n == 0 or n == 1:
        return n
    return F(n - 1) + F(n - 2)
print(F(100))