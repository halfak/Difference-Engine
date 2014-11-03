import mw

from jsonable import JSONable

from .delta import Delta
from .timestamp import Timestamp
from .user import User


class Revision(JSONable):
    __slots__ = ("rev_id", "timestamp", "sha1", "page_id", "user", "delta")
    
    def initialize(self, rev_id, timestamp, sha1, page_id, user, delta):
        self.rev_id = int(rev_id)
        self.timestamp = Timestamp(timestamp)
        self.sha1 = str(sha1)
        self.page_id = int(page_id)
        self.user = User(user)
        self.delta = Delta(delta)
