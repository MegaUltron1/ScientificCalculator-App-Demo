import math
import unittest

import advanced_operations as adv


class TestAdvancedOperations(unittest.TestCase):
    def test_sqrt(self) -> None:
        self.assertEqual(adv.sqrt(9), 3)

    def test_sqrt_domain_error(self) -> None:
        with self.assertRaises(ValueError):
            adv.sqrt(-1)

    def test_power(self) -> None:
        self.assertEqual(adv.power(2, 10), 1024)

    def test_trig(self) -> None:
        self.assertAlmostEqual(adv.sin(math.pi / 2), 1.0, places=12)
        self.assertAlmostEqual(adv.cos(0), 1.0, places=12)


if __name__ == "__main__":
    unittest.main()

