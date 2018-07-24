import unittest

from src.parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.p = Parser([])

    def test_empty_or_comment(self):
        self.assertTrue(self.p._empty_or_comment(''))
        self.assertTrue(self.p._empty_or_comment('#'))
        self.assertTrue(self.p._empty_or_comment('    #'))
        self.assertFalse(self.p._empty_or_comment('a = 5'))
        self.assertFalse(self.p._empty_or_comment(' a = 5'))