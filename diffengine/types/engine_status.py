from collections import defaultdict

from ..engines import Engine
from ..wiki import Wiki
from .jsonable_type import JsonableType
from .timestamp import Timestamp


class EngineStatus(JsonableType):
    __slots__ = ('engine_info', 'last_rev_id', 'last_timestamp', 'stats')
    
    def initiate(self, engine_info, last_rev_id=0, last_timestamp=None,
                       stats=None):
        
        self.engine_info = str(engine_info)
        
        self.update(last_rev_id, last_timestamp)
        
        self.stats = defaultdict(lambda: 0, stats or {})
    
    def update(self, last_rev_id, last_timestamp):
        self.last_rev_id = int(last_rev_id)
        self.last_timestamp = Timestamp(last_timestamp) \
                              if last_timestamp is not None \
                              else None
