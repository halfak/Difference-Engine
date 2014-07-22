from deltas import segment_matcher, Segmenter

from . import defaults
from .. import operations
from .jsonable_type import JsonableType


class SegmentMatcherProcessor(Processor):
    
    def __init__(self, tokenizer, segmenter):
        self.tokenizer   = tokenizer
        self.segmenter   = segmenter
    
    def process(self, rev_id, new_text):
        new_tokens = self.tokenizer.tokenize(text)
        
        deltas_ops = segment_matcher.diff(
            self.last_tokens,
            new_tokens,
            segmenter = self.segmenter
        )
        operations = list(Operation.from_delta_op(deltas_ops, self.last_tokens
                                                              new_tokens))
        
        
        old_text = "".join(self.last_tokens)
        
        chars = len(new_text) - len(old_text)
        bytes = len(bytes(new_text, 'utf-8', 'replace')) -
                len(bytes(old_text, 'utf-8', 'replace'))
        
        return Delta(chars, bytes, operations)

class SegmentMatcherEngine(DifferenceEngine):
    
    def __init__(self, tokenizer, segmenter):
        self.tokenizer = tokenizer
        self.segmenter = segmenter
    
    def process(self, last_tokens, new_text):
        new_tokens = self.tokenizer.tokenize(text)
        
        deltas_ops = segment_matcher.diff(
            self.last_tokens,
            new_tokens,
            segmenter = self.segmenter
        )
        operations = list(Operation.from_delta_op(deltas_ops, self.last_tokens
                                                              new_tokens))
        
        
        old_text = "".join(self.last_tokens)
        
        chars = len(new_text) - len(old_text)
        bytes = len(bytes(new_text, 'utf-8', 'replace')) -
                len(bytes(old_text, 'utf-8', 'replace'))
        
        return Delta(chars, bytes, operations)
        
        return delta
