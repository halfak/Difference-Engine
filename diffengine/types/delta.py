from jsonable import JSONable

from .operations import Operation


class Delta(JSONable):
    __slots__ = ("bytes", "chars", "operations")
    
    def initialize(self, bytes, chars, operations):
        self.bytes = int(bytes)
        self.chars = int(chars)
        self.operations = [Operation(op) for op in operations]
