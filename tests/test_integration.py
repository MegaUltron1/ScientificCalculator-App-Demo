import unittest

from calculator import CalculatorError, evaluate


class TestIntegration(unittest.TestCase):
    def test_expression_with_trig_and_addition(self) -> None:
        self.assertAlmostEqual(evaluate("1 + sin(pi/2)").value, 2.0, places=12)

    def test_expression_with_sqrt_and_power(self) -> None:
        self.assertEqual(evaluate("sqrt(10) + power(2,3)").value, 11.0)

    def test_power_alias_caret(self) -> None:
        self.assertEqual(evaluate("2^3").value, 8.0)

    def test_rejects_unsafe_names(self) -> None:
        with self.assertRaises(CalculatorError):
            evaluate("__import__('os').system('echo hi')")

    def test_rejects_attributes(self) -> None:
        with self.assertRaises(CalculatorError):
            evaluate("(1).real")


if __name__ == "__main__":
    unittest.main()

