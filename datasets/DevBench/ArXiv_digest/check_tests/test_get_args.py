import unittest
from query_arxiv import get_args

class TestGetArgs(unittest.TestCase):

    def test_defaults_only_recent_days(self) -> None:
        args = get_args([
            '--recent_days', '60'
        ])

        self.assertIsNone(args.category)
        self.assertIsNone(args.title)
        self.assertIsNone(args.author)
        self.assertIsNone(args.abstract)
        self.assertEqual(args.max_results, 10)
        self.assertEqual(args.recent_days, 60)
        self.assertEqual(args.to_file, "")
        self.assertFalse(args.verbose)