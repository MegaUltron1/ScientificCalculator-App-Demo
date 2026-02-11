import unittest

import basic_operations as basic


class TestBasicOperations(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(basic.add(2, 3), 5)

    def test_subtract(self) -> None:
        self.assertEqual(basic.subtract(10, 4), 6)

    def test_multiply(self) -> None:
        self.assertEqual(basic.multiply(6, 7), 42)

    def test_divide(self) -> None:
        self.assertEqual(basic.divide(8, 2), 4)

    def test_divide_by_zero(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            basic.divide(1, 0)


if __name__ == "__main__":
    unittest.main()

