from .jsonable_type import JsonableType
from .user import User
from .delta import Delta

class Revision(JsonableType):
    __slots__ = ("rev_id", "timestamp", "page_id", "user", "delta")
    
    def initiate(self, rev_id, timestamp, page_id, user, delta):
        self.rev_id = int(rev_id)
        self.timestamp = int(timestamp)
        self.page_id = int(page_id)
        self.user = User(user)
        self.delta = Delta(delta)
