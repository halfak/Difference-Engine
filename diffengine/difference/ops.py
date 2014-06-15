"""
A collection of operations necessary to represent a difference.
"""

from collections import namedtuple

Insert = namedtuple("Insert", ['start', 'end'])
Persist = namedtuple("Persist",   ['start', 'end'])
Remove = namedtuple("Remove", ['start', 'end'])
