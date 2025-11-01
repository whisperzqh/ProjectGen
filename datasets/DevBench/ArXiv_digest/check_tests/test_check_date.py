import unittest
from datetime import datetime
from query_arxiv import check_date

class TestCheckDate(unittest.TestCase):

    def test_within_range(self):
        """
        Test case where the submission date is within the range of recent_days from the current date.
        """
        date_string = "2023-01-01T00:00:00Z"
        recent_days = 8
        current_date = datetime(2023, 1, 9)  # This makes it exactly 10 days from the submission date
        result = check_date(date_string, recent_days, current_date)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
