import mw

from .jsonable_type import JsonableType

class Timestamp(mw.Timestamp):
    
    def to_json(self):
        return self.unix()
    
    @classmethod
    def from_json(cls, doc):
        return cls(doc)
