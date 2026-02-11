"""Advanced operations for the scientific calculator."""

import math


def sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("square root domain error (x must be >= 0)")
    return math.sqrt(x)


def power(base: float, exponent: float) -> float:
    return base**exponent


def sin(x: float) -> float:
    return math.sin(x)


def cos(x: float) -> float:
    return math.cos(x)


def tan(x: float) -> float:
    return math.tan(x)

