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

C = '''[hello]
test=a
'''


class TestCli(unittest.TestCase):
    """Test the CLI things."""

    def test_formatting_is_not_none(self):
        s = inidiff.cli.format_output(A, B)
        self.assertTrue(s is not None)

    def test_formatting_outputs_thing(self):
        s = inidiff.cli.format_output(A, B)
        self.assertTrue('thing' in s)

    def test_formatting_output_value_changed(self):
        s = inidiff.cli.format_output(A, B)
        self.assertTrue('-thing=b\n'
                        '+thing=c''' in s)

    def test_formatting_output_value_removed(self):
        s = inidiff.cli.format_output(B, C)
        print(s)
        self.assertTrue('-thing=c''' in s)
        self.assertTrue('+thing=''' not in s)
