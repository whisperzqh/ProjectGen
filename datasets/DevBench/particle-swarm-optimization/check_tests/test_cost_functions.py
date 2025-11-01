import unittest
import sys
import os

from pso.cost_functions import sphere


class TestCostFunctions(unittest.TestCase):

    def test_sphere(self):
        x = [1, 2, 4]
        result = sphere(x)
        self.assertEqual(result, 21)

        x = [1, 2, 0]
        result = sphere(x)
        self.assertEqual(result, 5)

        x = [-1, 2, -4]
        result = sphere(x)
        self.assertEqual(result, 21)


if __name__ == '__main__':
    unittest.main()