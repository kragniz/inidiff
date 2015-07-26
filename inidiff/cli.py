from __future__ import print_function

from . import diff

import argparse


def format_option(opt):
    """Return a formatted option in the form name=value."""
    return '{}={}\n'.format(opt.option, opt.value)


def format_output(first, second):
    """Return a string showing the differences between two ini strings."""
    diffs = diff(first, second)

    sections = set()
    out = ''
    for d in diffs:
        if d.first.section not in sections:
            out += '[{}]\n'.format(d.first.section)
            sections.add(d.first.section)
        if d.first.value is not None:
            out += '-' + format_option(d.first)
        if d.second.value is not None:
            out += '+' + format_option(d.second)

    return out


def main():
    """Run the main CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('first', type=argparse.FileType('r'))
    parser.add_argument('second', type=argparse.FileType('r'))
    args = parser.parse_args()

    first = args.first.read()
    second = args.second.read()

    print(format_output(first, second), end='')
