import mw

from jsonable import JSONable


class Timestamp(mw.Timestamp):
    
    def to_json(self):
        return self.short_format()
    
    @classmethod
    def from_json(cls, doc):
        return cls(doc)
