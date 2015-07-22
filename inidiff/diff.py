from six.moves import cStringIO
import six.moves.configparser as configparser


class PermissiveConfigParser(configparser.SafeConfigParser):
    """A SafeConfigParser that returns empty instead of erroring."""

    def options(self, section):
        if self.has_section(section):
            # old style python classes are dumb
            return configparser.SafeConfigParser.options(self, section)
        else:
            return []


def conf_from_str(conf_str):
    """Return a ConfigParser object from a string."""
    parser = PermissiveConfigParser()
    ini_str = cStringIO(conf_str)
    parser.readfp(ini_str)

    return parser


def diff(first, second):
    """Diff two ini files."""
    conf_first = conf_from_str(first)
    conf_second = conf_from_str(second)

    diffs = []

    sections = set(conf_first.sections() + conf_second.sections())
    for section in sections:
        options = set(conf_first.options(section) +
                      conf_second.options(section))
        for option in options:
            f = conf_first.get(section, option)
            s = conf_second.get(section, option)
            if f != s:
                diffs.append(((section, option, f), (section, option, s)))

    return diffs
