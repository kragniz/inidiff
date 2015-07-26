import unittest

import inidiff

INI_1 = '''[test]
number=10
'''

INI_2 = '''[test]
number=20
'''

INI_3 = '''[DEFAULT]
cat=alphie
'''

INI_4 = '''[DEFAULT]
cat=tim
'''

INI_5 = '''[DEFAULT]
cat=tim
dog=bob
'''

INI_6 = '''[DEFAULT]
cat=tim
dog=
'''

INI_7 = '''[say]
dog=woof
cat=meow
bird=tweet
'''

INI_8 = '''[say]
dog=woof
cat=meow
fox=doo
mouse=squeak
bird=tweet
cow=moo
'''

INI_9 = '''[say]
dog=woof
cat=nyaa~
mouse=squeak
bird=tweet
kitty=nyaaaaa~
cow=moo
'''

INI_10 = '''[say]
dog=woof

[new]
hello=hi
'''


class TestDiff(unittest.TestCase):
    """Test diffs diff things."""

    def test_no_differences(self):
        self.assertEqual([], inidiff.diff(INI_1, INI_1))

    def test_some_differences(self):
        self.assertTrue(len(inidiff.diff(INI_1, INI_2)) > 0)

    def test_number_is_different(self):
        diffs = inidiff.diff(INI_1, INI_2)
        self.assertEqual('number', diffs[0].first.option)

    def test_default_section(self):
        diffs = inidiff.diff(INI_3, INI_4)
        self.assertTrue(len(diffs) > 0)
        self.assertEqual('DEFAULT', diffs[0].first.section)

    def test_extra_option(self):
        diffs = inidiff.diff(INI_4, INI_5)
        self.assertEqual(1, len(diffs))

    def test_extra_option_reversed(self):
        diffs = inidiff.diff(INI_5, INI_4)
        self.assertEqual(1, len(diffs))

    def test_unset_option(self):
        diffs = inidiff.diff(INI_5, INI_6)
        self.assertEqual(1, len(diffs))
        self.assertEqual('', diffs[0].second.value)

    def test_unset_option_reversed(self):
        diffs = inidiff.diff(INI_6, INI_5)
        self.assertEqual(1, len(diffs))
        self.assertEqual('', diffs[0].first.value)

    def test_multiple_added(self):
        diffs = inidiff.diff(INI_7, INI_8)
        self.assertEqual(3, len(diffs))

    def test_multiple_added_and_changed(self):
        diffs = inidiff.diff(INI_8, INI_9)
        self.assertEqual(3, len(diffs))
        for d in diffs:
            if d.first.option == 'cat':
                self.assertEqual('meow', d.first.value)
                self.assertEqual('nyaa~', d.second.value)

            if d.first.option == 'kitty':
                self.assertEqual(None, d.first.value)
                self.assertEqual('nyaaaaa~', d.second.value)

            if d.first.option == 'fox':
                self.assertEqual('doo', d.first.value)
                self.assertEqual(None, d.second.value)

    def test_new_section(self):
        diffs = inidiff.diff(INI_9, INI_10)
        self.assertEqual(6, len(diffs))
