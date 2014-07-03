from .jsonable_type import JsonableType

class Operation(JsonableType):
    __slots__ = ("start", "end")
    OP = NotImplemented
    OPERATIONS = {}
    
    def initiate(self, start, end, op=None):
        self.start = int(start)
        self.end   = int(end)
    
    def __init__(self, *args, **kwargs): pass
    
    def to_json(self):
        doc = JsonableType.to_json(self)
        doc['op'] = self.OP
        return doc
    
    @classmethod
    def from_json(cls, doc):
        op = doc['op']
        return cls.get(op)(**doc)
    
    @classmethod
    def register(cls, operation):
        cls.OPERATIONS[operation.OP] = operation
    
    @classmethod
    def get(cls, op):
        return cls.OPERATIONS[op]
    
class OperationWithTokens(Operation):
    __slots__ = ("tokens",)
    
    def initiate(self, start, end, tokens, op=None):
        Operation.initiate(self, start, end)
        self.tokens = tokens
    

class Insert(OperationWithTokens):
    OP = "+"
Operation.register(Insert)

class Persist(Operation):
    OP = "="
Operation.register(Persist)

class Remove(OperationWithTokens):
    OP = "-"
Operation.register(Remove)
