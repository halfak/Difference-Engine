from deltas import segment_matcher, Segmenter

from . import defaults
from .. import operations
from .jsonable_type import JsonableType


class SegmentMatcherProcessor(Processor):
    
    def __init__(self, page_id, last_id, segmenter,
                       last_tokens=None):
        super().__init__(page_id, last_id)
        
        self.last_tokens = last_tokens or []
    
    def process(self, rev_id, new_text):
        new_tokens = self.tokenizer.tokenize(text)
        
        ops = segment_matcher.diff(
            self.last_tokens,
            new_tokens,
            segmenter = self.segmenter
        )
        self.last_tokens = tokens
        
        old_text = "".join(self.last_tokens)
        
        chars = len(new_text) - len(old_text)
        bytes = len(bytes(new_text, 'utf-8', 'replace')) -
                len(bytes(old_text, 'utf-8', 'replace'))
        
        return Delta(chars, bytes, operations)

class SegmentMatcherEngine(DifferenceEngine):
    
    def __init__(self, datastore, segmenter):
        self.segmenter = segmenter
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
