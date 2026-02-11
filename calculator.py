"""Scientific calculator (core API + safe expression evaluator).

Supports:
- basic ops: +, -, *, /
- power: ** (and ^ as alias)
- functions: sqrt, power, sin, cos, tan
- constants: pi, e
"""

from __future__ import annotations

import ast
import math
from dataclasses import dataclass
from typing import Any, Callable

import advanced_operations as adv
import basic_operations as basic


class CalculatorError(Exception):
    """Raised for invalid expressions and unsupported operations."""


_ALLOWED_BINOPS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: basic.add,
    ast.Sub: basic.subtract,
    ast.Mult: basic.multiply,
    ast.Div: basic.divide,
    ast.Pow: adv.power,
}

_ALLOWED_UNARYOPS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: lambda x: x,
    ast.USub: lambda x: -x,
}

_ALLOWED_NAMES: dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
}

_ALLOWED_FUNCS: dict[str, Callable[..., float]] = {
    "sqrt": adv.sqrt,
    "power": adv.power,
    "sin": adv.sin,
    "cos": adv.cos,
    "tan": adv.tan,
}


@dataclass(frozen=True)
class EvalResult:
    value: float

    def as_json(self) -> dict[str, Any]:
        return {"value": self.value}


def evaluate(expression: str) -> EvalResult:
    expr = (expression or "").strip()
    if not expr:
        raise CalculatorError("empty expression")
    expr = _normalize_expression(expr)

    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise CalculatorError("invalid syntax") from e

    value = _eval_node(tree.body)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise CalculatorError("expression did not evaluate to a number")
    return EvalResult(float(value))


def _normalize_expression(expr: str) -> str:
    # Common calculator alias: '^' for exponentiation.
    # This is a simple replacement; users should avoid bitwise XOR semantics.
    return expr.replace("^", "**")


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return float(node.value)
        raise CalculatorError("only numeric constants are allowed")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        fn = _ALLOWED_BINOPS.get(op_type)
        if fn is None:
            raise CalculatorError(f"operator not allowed: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return float(fn(left, right))

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        fn = _ALLOWED_UNARYOPS.get(op_type)
        if fn is None:
            raise CalculatorError(f"unary operator not allowed: {op_type.__name__}")
        return float(fn(_eval_node(node.operand)))

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return float(_ALLOWED_NAMES[node.id])
        raise CalculatorError(f"name not allowed: {node.id}")

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise CalculatorError("only simple function calls are allowed")
        fn = _ALLOWED_FUNCS.get(node.func.id)
        if fn is None:
            raise CalculatorError(f"function not allowed: {node.func.id}")
        if node.keywords:
            raise CalculatorError("keyword arguments are not allowed")
        args = [_eval_node(a) for a in node.args]
        try:
            return float(fn(*args))
        except (TypeError, ValueError, ZeroDivisionError) as e:
            raise CalculatorError(str(e)) from e

    # Disallow everything else (attributes, subscripts, comprehensions, etc.).
    raise CalculatorError(f"expression element not allowed: {type(node).__name__}")


def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: python calculator.py \"2+2\"')
        return 2
    try:
        result = evaluate(" ".join(argv[1:]))
    except CalculatorError as e:
        print(f"Error: {e}")
        return 1
    print(result.value)
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(_main(sys.argv))
