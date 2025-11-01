import os
import unittest
from hone import hone
from hone.utils import test_utils

dirname = os.path.dirname(os.path.dirname(__file__))
csv_A_path = os.path.join(dirname, "examples", "", "example_a.csv")
json_A_path = os.path.join(dirname, "examples", "", "example_a.json")


class TestHone(unittest.TestCase):
    def test_csv_1(self):
        h = hone.Hone()
        actual_result = h.convert(csv_A_path)
        expected_result = test_utils.parse_json_file(json_A_path)
        self.assertListEqual(actual_result, expected_result)
        




if __name__ == '__main__':
    unittest.main()
