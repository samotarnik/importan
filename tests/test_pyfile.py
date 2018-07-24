import unittest

from src.pyfile import Pyfile
from tests import TESTS_ROOT


class TestPyfile(unittest.TestCase):

    def test_relative(self):
        pyfile = Pyfile('/a/b/c/d.py', '/a/b')
        self.assertEqual(pyfile.relative, 'c/d.py')
        pyfile = Pyfile('/a/b/c.py', '/a/')
        self.assertEqual(pyfile.relative, 'b/c.py')

    def test_module(self):
        pyfile = Pyfile('/a/b/c/d.py', '/a')
        self.assertEqual(pyfile.module, 'b.c.d')

    def test_representation(self):
        pyfile = Pyfile('/a/b/c/d.py', '/a')
        self.assertEqual(repr(pyfile), 'b/c/d.py')

    def test_lines(self):
        filename = TESTS_ROOT + '/fixtures/a.py'
        pyfile = Pyfile(filename, TESTS_ROOT)
        self.assertEqual(len(pyfile.lines()), 5)
