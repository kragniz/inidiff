import unittest

import inidiff

INI_1 = '''[test]
number=10
'''


class TestDiff(unittest.TestCase):
    """Test diffs diff things."""

    def test_no_differences(self):
        self.assertEqual([], inidiff.diff(INI_1, INI_1))
