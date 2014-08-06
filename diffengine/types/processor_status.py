import time
from collections import defaultdict

from jsonable import JSONable

from ..errors import RevisionOrderError
from .timestamp import Timestamp


class ProcessorStatus(JSONable):
    __slots__ = ('page_id', 'last_rev_id', 'last_timestamp', 'stats')
    
    def initialize(self, page_id, last_rev_id=0, last_timestamp=None,
                   stats=None):
        self.page_id        = int(page_id)
        self.last_rev_id    = int(last_rev_id)
        self.last_timestamp = Timestamp(last_timestamp) \
                              if last_timestamp != None \
                              else None
        self.stats          = defaultdict(lambda: 0, stats or {})
        
    def processed(self, rev_id, timestamp):
        self.check_order(rev_id, timestamp)
        self.set_state(rev_id, timestamp)
        self._increment_revisions()
    
    def _increment_revisions(self):
        self.stats['revisions_processed'] += 1
    
    def check_order(self, rev_id, timestamp):
        if self.last_timestamp is not None and \
           (self.last_timestamp, self.last_rev_id) >= (timestamp, rev_id):
                raise RevisionOrderError(
                        (self.last_timestamp, self.last_rev_id),
                        (timestamp, rev_id))
    
    def set_state(self, last_rev_id, last_timestamp, **stats):
        
        self.last_rev_id = int(last_rev_id)
        self.last_timestamp = Timestamp(last_timestamp) \
                              if last_timestamp != None \
                              else None
        
        self.stats.update(**stats)
        self.stats['last_updated'] = time.time()
