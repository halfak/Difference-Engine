from collections import defaultdict

from jsonable import AbstractJSONable, JSONable

from ..wiki import Wiki
from .timestamp import Timestamp


class EngineStatus(AbstractJSONable):
    __slots__ = ('engine_info', 'last_rev_id', 'last_timestamp', 'stats')
    
    def initialize(self, engine_info, last_rev_id=0, last_timestamp=None,
                         stats=None):
        
        self.engine_info = str(engine_info)
        
        self.update(last_rev_id, last_timestamp)
        
        self.stats = defaultdict(lambda: 0, stats or {})
    
    def update(self, last_rev_id, last_timestamp):
        self.last_rev_id = int(last_rev_id)
        self.last_timestamp = Timestamp(last_timestamp) \
                              if last_timestamp is not None \
                              else None
