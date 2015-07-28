from collections import namedtuple

from six.moves import cStringIO
import six.moves.configparser as configparser
from ordered_set import OrderedSet


Diff = namedtuple('Diff', 'first, second')
Option = namedtuple('Option', 'section, option, value')


class PermissiveConfigParser(configparser.RawConfigParser):
    """A RawConfigParser that returns empty instead of erroring."""

    def options(self, section):
        if self.has_section(section):
            # old style python classes are dumb
            return configparser.RawConfigParser.options(self, section)
        else:
            return []

    def get(self, *args, **kwargs):
        try:
            value = configparser.RawConfigParser.get(self, *args, **kwargs)
        except (configparser.NoOptionError, configparser.NoSectionError):
            value = None
        return value

    def clear_defaults(self):
        self._defaults = {}


def conf_from_str(conf_str):
    """Return a ConfigParser object from a string."""
    parser = PermissiveConfigParser()
    ini_str = cStringIO(conf_str)
    parser.readfp(ini_str)

    return parser


def _lower_or_none(string):
    try:
        return string.lower()
    except AttributeError:
        return None


def check_option(conf_first, conf_second, section, option, ignore_case=False):
    """Return a Diff namedtuple if the option differers between configs."""
    first = conf_first.get(section, option)
    second = conf_second.get(section, option)

    if ignore_case is True:
        first_lower = _lower_or_none(first)
        second_lower = _lower_or_none(second)

        different = (first_lower != second_lower)
    else:
        different = (first != second)

    if different:
        return Diff(Option(section, option, first),
                    Option(section, option, second))


def diff(first, second, ignore_case=False):
    """Diff two ini files."""
    conf_first = conf_from_str(first)
    conf_second = conf_from_str(second)

    diffs = []

    default_options = OrderedSet(list(conf_first.defaults().keys()) +
                                 list(conf_second.defaults().keys()))
    for option in default_options:
        section = 'DEFAULT'
        diff = check_option(conf_first, conf_second, section, option,
                            ignore_case)
        if diff is not None:
            diffs.append(diff)

    conf_first.clear_defaults()
    conf_second.clear_defaults()

    sections = OrderedSet(conf_first.sections() + conf_second.sections())
    for section in sections:
        options = OrderedSet(conf_first.options(section) +
                             conf_second.options(section))
        for option in options:
            diff = check_option(conf_first, conf_second, section, option,
                                ignore_case)
            if diff is not None:
                diffs.append(diff)

    return diffs
