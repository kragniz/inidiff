"""inidiff - Find the differences between two ini config files."""

from .diff import diff
from .cli import main

__version__ = '0.1.0'
__author__ = 'Louis Taylor <louis@kragniz.eu>'
__all__ = (diff, main)
