from . import diff

import argparse


def format_option(opt):
    """Return a formatted option in the form name=value."""
    return '{}={}\n'.format(opt.option, opt.value)


def format_output(first, second):
    """Return a string showing the differences between two ini strings."""
    diffs = diff(first, second)

    out = ''
    for d in diffs:
        if d.first.value is not None:
            out += '-' + format_option(d.first)
        if d.second.value is not None:
            out += '+' + format_option(d.second)

    return out


def main():
    """Run the main CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('first')
    parser.add_argument('second')
    args = parser.parse_args()

    print(format_output(args.first, args.second))
