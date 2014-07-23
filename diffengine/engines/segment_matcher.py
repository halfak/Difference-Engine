from deltas import segment_matcher, Segmenter

from ..types import Operation, EngineStatus, Delta
from .engine import Engine

class SegmentMatcherStatus(EngineStatus):
    
    def initiate(self, last_rev_id, last_tokens=None, **kwargs):
        super().initiate(last_rev_id, **kwargs)
        
        self.last_tokens = last_tokens or []
    
    def update(self, rev_id, timestamp, tokens):
        super().update(rev_id, timestamp)
        self.last_tokens = tokens
    

class SegmentMatcher(Engine):
    
    def __init__(self, status, tokenizer, segmenter):
        self.status    = SegmentMatcherStatus(status)
        self.tokenizer = tokenizer
        self.segmenter = segmenter
        
        self.last_text = "".join(self.status.last_tokens)
    
    def process(self, rev_id, timestamp, new_text):
        if rev_id < self.status.last_rev_id:
            raise RevisionOrderError(self.status.last_rev_id, rev_id)
        
        new_tokens = self.tokenizer.tokenize(new_text)
        
        deltas_ops = segment_matcher.diff(
            self.status.last_tokens,
            new_tokens,
            segmenter = self.segmenter
        )
        operations = [Operation.from_delta_op(op, self.status.last_tokens,
                                              new_tokens)
                      for op in deltas_ops]
        
        char_diff = len(new_text) - len(self.last_text)
        byte_diff = len(bytes(new_text, 'utf-8', 'replace')) - \
                    len(bytes(self.last_text, 'utf-8', 'replace'))
        
        delta = Delta(segment_matcher.__name__, char_diff, byte_diff, operations)
        
        self.status.update(rev_id, timestamp, new_tokens)
        self.last_text = new_text
        
        return delta
