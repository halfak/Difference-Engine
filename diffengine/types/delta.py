from .jsonable_type import JsonableType
from .operations import Operation

class Delta(JsonableType):
    __slots__ = ("algorithm", "bytes", "chars", "operations")
    
    def initiate(self, algorithm, bytes, chars, operations):
        self.algorithm = str(algorithm)
        self.bytes = int(bytes)
        self.chars = int(chars)
        self.operations = [Operation(op) for op in operations]
    
    
