from collections import Iterable

class LookAhead:
    
    class DONE: pass
    
    def __new__(cls, it):
        if isinstance(it, cls):
            return it
        elif hasattr(it, "__next__") or hasattr(it, "__iter__"):
            return cls.from_iterable(it)
        else:
            raise TypeError("Expected iterable, got {0}", type(it))
    
    @classmethod
    def from_iterable(cls, iterable):
        instance = super().__new__(cls)
        instance.initialize(iterable)
        return instance
    
    def __init__(self, *args, **kwargs): pass
    
    def initialize(self, iterable):
        self.iterable = iter(iterable)
        
        self._load_next()
        
    def _load_next(self):
        try:
            self.next = next(self.iterable)
        except StopIteration:
            self.next = self.DONE
    
    def __iter__(self): return self
    
    def __next__(self):
        if self.empty():
            raise StopIteration()
        else:
            current = self.next
            self._load_next()
            return current
    
    def pop(self):
        return self.__next__()
    
    def peek(self):
        return self.next
    
    def empty(self):
        return self.next == self.DONE
