import argparse
import os
from io import StringIO
import unittest
from unittest.mock import patch,mock_open
import sys

from lice import core
from lice.core import (
    LICENSES, clean_path, extract_vars, generate_license,
    format_license,get_suffix,load_file_template, 
    load_template,valid_year)


class TestFormatLicense(unittest.TestCase):
    def test_format_license_python_language(self):
        license_text = StringIO("Test License Text")
        formatted_text = format_license(license_text, "py").getvalue()
        expected_output = "\n# Test License Text\n"
        self.assertEqual(formatted_text, expected_output)

class TestGetSuffix(unittest.TestCase):
    def test_valid_suffix(self):
        filename = "test.py"
        self.assertEqual(get_suffix(filename), "py")

class TestValidYear(unittest.TestCase):
    def test_valid_year(self):
        self.assertEqual(valid_year("2025"), "2025")

class TestMainFunction(unittest.TestCase):
    def test_valid_license(self):
        test_args = ["program", "apache"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=StringIO):
                core.main()

    def test_list_languages_option(self):
        test_args = ["program", "--languages"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with self.assertRaises(SystemExit) as cm:
                    core.main()
                self.assertEqual(cm.exception.code, 0)
                output = mock_stdout.getvalue()
                self.assertIn("java", output)

    def test_output_to_file(self):
        test_args = ["program", "apache", "-f", "test_output.txt"]
        with patch.object(sys, 'argv', test_args):
            with patch("builtins.open", new_callable=mock_open()) as mock_file:
                core.main()
                mock_file.assert_called_with("test_output.txt", "w")

    def test_list_template_vars(self):
            test_args = ["program", "apache", "--vars"]
            expected_output = "The apache license template contains the following variables"

            with patch.object(sys, 'argv', test_args):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    with self.assertRaises(SystemExit):
                        core.main()
                    output = mock_stdout.getvalue()
                    self.assertIn(expected_output, output)


if __name__ == '__main__':
    unittest.main()
