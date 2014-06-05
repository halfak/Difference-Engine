
from . import defaults
from .. import ops, sequence_matcher
from ..difference_engine import DifferenceEngine
from .difference import diff


class HierarchicalMatcher(DifferenceEngine):
    def __init__(self,
                 tokenizer=defaults.TOKENIZER,
                 last=None,
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
