from unittest import TestCase
from argparse import ArgumentTypeError

import mock

import arithmetic_computing.helper.arguments_parser as arguments_parser


class TestArgumentsParser(TestCase):

    def test_check_processes_too_big(self):
        with self.assertRaises(ArgumentTypeError):
            arguments_parser.check_processes("11")

    def test_check_processes_too_small(self):
        with self.assertRaises(ArgumentTypeError):
            arguments_parser.check_processes("0")

    def test_check_processes_not_int(self):
        with self.assertRaises(ValueError):
            arguments_parser.check_processes("test")

    def test_check_processes(self):
        result = arguments_parser.check_processes("5")
        self.assertEqual(result, 5)


