import mw

from .jsonable_type import JsonableType
from .user import User
from .delta import Delta

class Timestamp(mw.Timestamp):
    
    def to_json(self):
        return self.unix()
    
    @classmethod
    def from_json(cls, doc):
        return cls(int(doc))

class Revision(JsonableType):
    __slots__ = ("rev_id", "timestamp", "page_id", "user", "delta")
    
    def initiate(self, rev_id, timestamp, page_id, user, delta):
        self.rev_id = int(rev_id)
        self.timestamp = Timestamp(timestamp)
        self.page_id = int(page_id)
        self.user = User(user)
        self.delta = Delta(delta)
