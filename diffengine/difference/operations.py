"""
A collection of operations necessary to represent a difference.
"""
class Operation:
    __slots__ = ("start", "end")
    def __init__(self, start, end):
        self.start = int(start)
        self.end   = int(end)

class Insert(Operation): pass
class Persist(Operation): pass
class Remove(Operation): pass
