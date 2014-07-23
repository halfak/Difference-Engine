import time
from collections import defaultdict

from .jsonable_type import JsonableType
from .timestamp import Timestamp

class EngineStatus(JsonableType):
    __slots__ = ('page_id', 'last_rev_id', 'last_timestamp', 'stats')
    
    def initiate(self, page_id, last_rev_id=0, last_timestamp=None, stats=None):
        self.page_id        = int(page_id)
        self.last_rev_id    = int(last_rev_id)
        self.last_timestamp = Timestamp(last_timestamp) \
                              if last_timestamp != None \
                              else None
        self.stats          = defaultdict(lambda: 0, stats or {})
        
    def update(self, rev_id, timestamp):
        
        self.stats['revisions_processed'] += 1
        self.stats['last_updated'] = time.time()
        self.last_rev_id = rev_id
        self.last_timestamp = timestamp
    
