"""
Roughly matches the operations from `deltas`, but includes tokens in the case of
insert and delete. TODO

.. role:: python(code)
   :language: python

:Examples:
    :python:`Insert(0, 6, 0, 6, tokens=["Foo", " ", "bar", " ", "herp", " ", "derp"])`:
        .. code-block:: python
        
            {
                "opname": "insert",
                "a1": 0,
                "a2": 6,
                "b1": 0,
                "b2": 6
                "tokens": ["Foo", " ", "bar", " ", "herp", " ", "derp"]
            }
    
    :python:`Delete(0, 6, 0, 0, tokens=["Foo", " ", "bar", " ", "herp", " ", "derp"])`:
        .. code-block:: python
        
            {
                "opname": "delete",
                "a1": 0,
                "a2": 6,
                "b1": 0,
                "b2": 0
                "tokens": ["Foo", " ", "bar", " ", "herp", " ", "derp"]
            }
    
    :python:`Equal(0, 6, 0, 6)`:
        .. code-block:: python
        
            {
                "opname": "equal",
                "a1": 0,
                "a2": 6,
                "b1": 0,
                "b2": 6
            }
"""
from .jsonable_type import JsonableType
import deltas


class Operation(JsonableType):
    __slots__ = ('a1', 'a2', 'a3', 'a4')
    
    OPERATIONS = {}
    OP = NotImplemented
    
    def initiate(self, a1, a2, b1, b2):
        self.a1 = int(a1)
        self.a2 = int(a2)
        self.b1 = int(b1)
        self.b2 = int(b2)
    
    def to_json(self):
        doc = JsonableType.to_json(self)
        doc['op'] = self.OP
    
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
    
    @classmethod
    def from_delta_op(cls, delta_op, a, b):
        OperationClass = cls.get(operation.opname)
        return OperationClass.from_delta_op(operation, a, b)
    
class OperationWithTokens(Operation):
    
    __slots__ = ('tokens', )
    
    def initiate(self, *args, tokens):
        super().__init__(*args)
        self.tokens = tokens
    

class Insert(OperationWithTokens):
    
    OP = "+"
    
    @classmethod
    def from_delta_op(cls, delta_op, a, b):
        return cls(*delta_op, tokens=b[delta_op.b1:delta_op.b2])
    
Operation.register(Insert)

class Equal(Operation):
    
    OP = "="
    
    @classmethod
    def from_delta_op(cls, delta_op, a, b):
        return cls(*delta_op, tokens=b[delta_op.b1:delta_op.b2])

Operation.register(Equal)

class Delete(OperationWithTokens):
    
    OP = "-"
    
    @classmethod
    def from_delta_op(cls, delta_op, a, b):
        return cls(*delta_op, tokens=a[delta_op.a1:delta_op.a2])

Operation.register(Delete)
