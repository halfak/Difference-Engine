from . import instance


class SelfConstructor:
    
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            if isinstance(args[0], cls):
                inst = args[0]
            else:
                inst = super().__new__(cls)
                inst.initiate(args[0])
        else:
            inst = super().__new__(cls)
            inst.initiate(*args, **kwargs)
        
        return inst
    
    def __init__(self, *args, **kwargs): pass
    
    def initiate(self, *args, **kwargs): raise NotImplementedError()
    
    def __str__(self): return self.__repr__()
    def __repr__(self):
        return instance.kwargs_slots_repr(self)
