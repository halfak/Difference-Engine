from collections import defaultdict
from .jsonable_type import JsonableType

class Processor(JsonableType):
    
    def initialize(self, page_id, last_id=0):
        self.page_id = int(page_id)
        self.last_rev_id = int(last_id)
    
    def process(self, rev_id, text): raise NotImplementedError()
