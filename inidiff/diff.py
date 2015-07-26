from collections import namedtuple

from six.moves import cStringIO
import six.moves.configparser as configparser
from ordered_set import OrderedSet


Diff = namedtuple('Diff', 'first, second')
Option = namedtuple('Option', 'section, option, value')


class PermissiveConfigParser(configparser.SafeConfigParser):
    """A SafeConfigParser that returns empty instead of erroring."""

    def options(self, section):
        if self.has_section(section):
            # old style python classes are dumb
            return configparser.SafeConfigParser.options(self, section)
        else:
            return []

    def get(self, *args, **kwargs):
        try:
            value = configparser.SafeConfigParser.get(self, *args, **kwargs)
        except configparser.NoOptionError:
            value = None
        return value


def conf_from_str(conf_str):
    """Return a ConfigParser object from a string."""
    parser = PermissiveConfigParser()
    ini_str = cStringIO(conf_str)
    parser.readfp(ini_str)

    return parser


def check_option(conf_first, conf_second, section, option):
    """Return a Diff namedtuple if the option differers between configs."""
    first = conf_first.get(section, option)
    second = conf_second.get(section, option)
    if first != second:
        return Diff(Option(section, option, first),
                    Option(section, option, second))


def diff(first, second):
    """Diff two ini files."""
    conf_first = conf_from_str(first)
    conf_second = conf_from_str(second)

    diffs = []

    default_options = OrderedSet(list(conf_first.defaults().keys()) +
                                 list(conf_second.defaults().keys()))
    for option in default_options:
        section = 'DEFAULT'
        diff = check_option(conf_first, conf_second, section, option)
        if diff is not None:
            diffs.append(diff)

    sections = OrderedSet(conf_first.sections() + conf_second.sections())
    for section in sections:
        options = OrderedSet(conf_first.options(section) +
                             conf_second.options(section))
        for option in options:
            diff = check_option(conf_first, conf_second, section, option)
            if diff is not None:
                diffs.append(diff)

    return diffs
