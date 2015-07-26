import unittest

import inidiff

A = '''[hello]
test=a
thing=b
'''

B = '''[hello]
test=a
thing=c
'''


class TestCli(unittest.TestCase):
    """Test the CLI things."""

    def test_formatting_is_not_none(self):
        s = inidiff.cli.format_output(A, B)
        self.assertTrue(s is not None)

    def test_formatting_output(self):
        s = inidiff.cli.format_output(A, B)
        self.assertTrue('thing' in s)
