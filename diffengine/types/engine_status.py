from collections import defaultdict
from .jsonable_type import JsonableType

class EngineStatus(JsonableType):
    
    def initialize(self, page_id, last_rev_id=0, last_timestamp=None, stats=None):
        self.page_id        = int(page_id)
        self.last_rev_id    = int(last_rev_id)
        self.stats          = defaultdict(stats, lambda: 0) \
                              if stats is not None
                              else defaultdict({}, lambda: 0)
        
    def update(self, rev_id, timestamp):
        
        self.stats['revisions_processed'] += 1
        self.stats['last_updated'] = time.time()
        self.stats['last_timestamp'] = timestamp
        self.last_rev_id = rev_id
