from __future__ import print_function

import argparse
import sys

from . import diff


RED = '\033[1;31m'
GREEN = '\033[1;32m'
END = '\033[0m'


def format_option(opt):
    """Return a formatted option in the form name=value."""
    return '{}={}\n'.format(opt.option, opt.value)


def format_output(first, second, color=True, ignore_case=False):
    """Return a string showing the differences between two ini strings."""
    diffs = diff(first, second, ignore_case=ignore_case)

    sections = set()
    out = ''
    for d in diffs:
        if d.first.section not in sections:
            out += '\n[{}]\n'.format(d.first.section)
            sections.add(d.first.section)
        if d.first.value is not None:
            if color:
                out += RED
            out += '-' + format_option(d.first)
            if color:
                out += END

        if d.second.value is not None:
            if color:
                out += GREEN
            out += '+' + format_option(d.second)
            if color:
                out += END

    return out


def main():
    """Run the main CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('first', type=argparse.FileType('r'),
                        help='First ini file')
    parser.add_argument('second', type=argparse.FileType('r'),
                        help='Second ini file')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='ignore case for values')
    parser.add_argument('--no-color', action='store_true',
                        help='don\'t show color')
    args = parser.parse_args()

    first = args.first.read()
    second = args.second.read()

    out = format_output(first, second, color=not args.no_color,
                        ignore_case=args.ignore_case)
    print(out.strip(), end='')

    if out:
        sys.exit(1)
