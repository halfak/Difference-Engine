import inspect
from itertools import chain

JSON_TYPES = {str, int, float}

class JsonableType:
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            if isinstance(args[0], cls):
                inst = args[0]
            elif isinstance(args[0], dict):
                inst = cls.from_json(args[0])
            else:
                inst = super().__new__(cls)
                inst.initiate(args[0])
        else:
            inst = super().__new__(cls)
            inst.initiate(*args, **kwargs)
        
        return inst
    
    def __init__(self, *args, **kwargs): pass
    
    def initiate(self, *args, **kwargs): raise NotImplementedError()
    
    def __eq__(self, other):
        if other == None: return False
        try:
            for key in self.keys():
                    if getattr(self, key) != getattr(other, key): return False
            
            return True
        except KeyError:
            return False
        
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __str__(self): return self.__repr__()
    
    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            ", ".join(
                "%s=%r" % (k, v) for k, v in self.items()
            )
        )
    
    def items(self):
        for key in self.keys():
            yield key,getattr(self, key)
    
    def keys(self):
        return chain(*(getattr(cls, '__slots__', [])
                       for cls in self.__class__.__mro__))
                              
    
    def to_json(self):
        return {k:self._to_json(v) for k, v in self.items()}
    
    @classmethod
    def _to_json(cls, value):
        print(value)
        if type(value) in JSON_TYPES:
            return value
        elif hasattr(value, "to_json"):
            return value.to_json()
        elif isinstance(value, list):
            return [cls._to_json(v) for v in value]
        elif isinstance(value, dict):
            return {str(k):cls._to_json(v) for k,v in value.items()}
        else:
            raise TypeError("{0} is not json serializable.".format(type(value)))

    @classmethod
    def from_json(cls, doc):
        return cls(**doc)
    
        
