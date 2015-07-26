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

D = '''[hello]
test=a
two=2
'''

E = '''[hello]
test=a
two=2
three=3
four=4
five=5
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
        self.assertTrue('-thing=c''' in s)
        self.assertTrue('+thing=''' not in s)

    def test_formatting_output_value_added(self):
        s = inidiff.cli.format_output(C, D)
        self.assertTrue('+two=2''' in s)
        self.assertTrue('-two=''' not in s)
        self.assertTrue('test=''' not in s)

    def test_formatting_section_with_one_change(self):
        s = inidiff.cli.format_output(C, D)
        print(s)
        self.assertTrue('[hello]\n+two=2''' in s)
        self.assertTrue('-two=''' not in s)
        self.assertTrue('test=''' not in s)

    def test_formatting_section_in_order(self):
        s = inidiff.cli.format_output(D, E)
        self.assertTrue('[hello]\n+three=3\n+four=4\n+five=5''' in s)
