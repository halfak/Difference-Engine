from collections import defaultdict

from ..engines import Engine
from ..wiki import Wiki
from .jsonable_type import JsonableType
from .timestamp import Timestamp

class SyncContinue(JsonableType):
    
    TYPE = NotImplemented
    CONTINUES = {}
    
    def to_json(self):
        doc = super().to_json()
        doc['type'] = self.TYPE
        return doc
    
    @classmethod
    def register(cls, continue_class):
        cls.CONTINUES[continue_class.TYPE] = continue_class
    
    @classmethod
    def from_json(cls, doc):
        continue_class = cls.CONTINUES[doc['type']]
        
        return continue_class.from_json(doc)
    
class DumpContinue(SyncContinue):
    __slots__ = ('last_rev_id', 'last_timestamp')
    TYPE = "dump"
    
    def initiate(self, last_rev_id, last_timestamp, type=None):
        self.last_rev_id = int(last_rev_id)
        self.last_timestamp = Timestamp(last_timestamp)
    
    @classmethod
    def from_json(cls, doc):
        return cls(**doc)
    
SyncContinue.register(DumpContinue)
    
class APIContinue(SyncContinue):
    __slots__ = ('query_continue', 'last_timestamp')
    TYPE = "api"
    
    def initiate(self, query_continue, last_timestamp, type=None):
        self.query_continue = query_continue
        self.last_timestamp = Timestamp(last_timestamp)
    
    @classmethod
    def from_json(cls, doc):
        return cls(**doc)
    
SyncContinue.register(APIContinue)

class SyncStatus(JsonableType):
    __slots__ = ('name', 'wiki_name', 'engine_info', 'sync_continue', 'stats')
    
    def initiate(self, name, wiki_name, engine_info, sync_continue,
                       stats=None):
        self.name = str(name)
        
        self.wiki_name = str(wiki_name)
        
        self.engine_info = str(engine_info)
        
        self.sync_continue  = SyncContinue(sync_continue)
        
        self.stats          = defaultdict(lambda: 0, stats or {})
