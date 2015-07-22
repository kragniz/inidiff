import unittest

import inidiff

INI_1 = '''[test]
number=10
'''

INI_2 = '''[test]
number=20
'''


class TestDiff(unittest.TestCase):
    """Test diffs diff things."""

    def test_no_differences(self):
        self.assertEqual([], inidiff.diff(INI_1, INI_1))

    def test_some_differences(self):
        self.assertTrue(len(inidiff.diff(INI_1, INI_2)) > 0)

    def test_number_is_different(self):
        diffs = inidiff.diff(INI_1, INI_2)
        first, second = diffs[0]
        self.assertEqual('number', first[1])
