from .jsonable_type import JsonableType
from .operations import Operation


class Delta(JsonableType):
    __slots__ = ("bytes", "chars", "operations")
    
    def initiate(self, bytes, chars, operations):
        self.bytes = int(bytes)
        self.chars = int(chars)
        self.operations = [Operation(op) for op in operations]
