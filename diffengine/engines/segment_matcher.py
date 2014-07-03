
from . import defaults
from .. import ops, sequence_matcher
from ..difference_engine import DifferenceEngine
from ..difference.segmentation_matcher import diff
from .jsonable_type import JsonableType


class SegmentMatcherProcessor(Processor):
    
    def __init__(self, page_id, last_id, tokenizer, segmenter,
                       last_tokens=None):
        super().__init__(page_id, last_id)
        
        self.last_tokens = last_tokens or []
    
    def process(self, rev_id, new_text):
        new_tokens = self.tokenizer.tokenize(text)
        
        ops = diff(
            self.last_tokens,
            new_tokens,
            tokenizer=self.tokenizer,
            min_group_size=self.min_group_size
        )
        self.last_tokens = tokens
        
        old_text = "".join(self.last_tokens)
        
        chars = len(new_text) - len(old_text)
        bytes = len(bytes(new_text, 'utf-8', 'replace')) -
                len(bytes(old_text, 'utf-8', 'replace'))
        
        return Delta(chars, bytes, operations)
        
        
    def update(self, rev_id):
        

class SegmentMatcher(DifferenceEngine):
    def __init__(self,
                 status,
                 tokenizer=defaults.TOKENIZER,
                 min_group_size=defaults.MIN_GROUP_SIZE):
        self.tokenizer = tokenizer
        self.last = last or []
        self.min_group_size = int(min_group_size)
    
    def process(self, tokens):
        delta = diff(
            self.last,
            tokens,
            tokenizer=self.tokenizer,
            min_group_size=self.min_group_size
        )
        self.last = tokens
        
        return delta
