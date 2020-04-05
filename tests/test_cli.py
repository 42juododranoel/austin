from argparse import ArgumentParser
import contextlib
import io
import unittest

from austin.cli import get_argument_parser

EXPECTED_HELP = """
usage: python3 -m unittest [-h] [--branch BRANCH] [--start-date START_DATE]
                           [--end-date END_DATE]
                           url

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  --branch BRANCH
  --start-date START_DATE
                        YYYY-MM-DD
  --end-date END_DATE   YYYY-MM-DD
"""[1:]  # Non first newline


class TestGetArgumentParser(unittest.TestCase):
    def setUp(self):
        self.parser = get_argument_parser()

    def test_return_parser(self):
        self.assertIsInstance(self.parser, ArgumentParser)

    def test_print_help(self):
        with io.StringIO() as buffer:
            with contextlib.redirect_stdout(buffer):
                self.parser.print_help()
            stdout = buffer.getvalue()

        self.assertEqual(stdout, EXPECTED_HELP)


class TestParseArguments(unittest.TestCase):
    def setUp(self):
        self.parser = get_argument_parser()

    def test_parse_url(self):
        arguments = ['https://github.com/octocat/Hello-World']

        namespace = self.parser.parse_args(arguments)

        self.assertEqual(namespace.url, arguments[0])

    def test_parse_branch(self):
        arguments = ['https://github.com/octocat/Hello-World', '--branch', 'master']

        namespace = self.parser.parse_args(arguments)

        self.assertEqual(namespace.url, arguments[0])

    def test_parse_start_date(self):
        arguments = ['https://github.com/octocat/Hello-World', '--start-date', '1970-01-01']

        namespace = self.parser.parse_args(arguments)

        self.assertEqual(namespace.url, arguments[0])

    def test_parse_end_date(self):
        arguments = ['https://github.com/octocat/Hello-World', '--end-date', '1970-01-31']

        namespace = self.parser.parse_args(arguments)

        self.assertEqual(namespace.url, arguments[0])
