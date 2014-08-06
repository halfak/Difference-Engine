import logging

from deltas import segment_matcher

from ..errors import RevisionOrderError
from ..segmenters import Segmenter
from ..tokenizers import Tokenizer
from ..types import Delta, EngineStatus, Operation, ProcessorStatus
from ..wiki import Wiki
from .engine import Engine, Processor

logger = logging.getLogger("diffengine.engines.segment_matcher")


class SegmentMatcherProcessorStatus(ProcessorStatus):
    __slots__ = ('last_tokens',)
    def initialize(self, page_id, last_rev_id=0, last_tokens=None, **kwargs):
        super().initialize(page_id, last_rev_id, **kwargs)
        
        self.last_tokens = last_tokens or []
    
    def processed(self, rev_id, timestamp, tokens):
        self.set_state(rev_id, timestamp, tokens)
        self._increment_revisions()
    
    def set_state(self, last_rev_id, last_timestamp, last_tokens, **stats):
        super().set_state(last_rev_id, last_timestamp, **stats)
        self.last_tokens = last_tokens
    

class SegmentMatcherProcessor(Processor):
    
    Status = SegmentMatcherProcessorStatus
    
    def __init__(self, status, tokenizer, segmenter):
        super().__init__(status)
        self.tokenizer = tokenizer
        self.segmenter = segmenter
    
    def set_status(self, status):
        self.status = SegmentMatcherProcessorStatus(status)
        self.last_text = "".join(self.status.last_tokens)
    
    def process(self, rev_id, timestamp, text):
        self.status.check_order(rev_id, timestamp)
        
        tokens = self.tokenizer.tokenize(text)
        
        deltas_ops = segment_matcher.diff(
            self.status.last_tokens,
            tokens,
            segmenter = self.segmenter
        )
        operations = [Operation.from_delta_op(op, self.status.last_tokens,
                                              tokens)
                      for op in deltas_ops]
        
        char_diff = len(text) - len(self.last_text)
        byte_diff = len(bytes(text, 'utf-8', 'replace')) - \
                    len(bytes(self.last_text, 'utf-8', 'replace'))
        
        delta = Delta(char_diff, byte_diff, operations)
        
        self.status.processed(rev_id, timestamp, tokens)
        self.last_text = text
        
        return delta

class SegmentMatcherStatus(EngineStatus): pass

class SegmentMatcher(Engine):
    
    Status = SegmentMatcherStatus
    Processor = SegmentMatcherProcessor
    
    def __init__(self, name, wiki, tokenizer, segmenter):
        super().__init__(name, wiki)
        self.tokenizer = tokenizer
        self.segmenter = segmenter
    
    
    def processor(self, status):
        return self.Processor(status, self.tokenizer, self.segmenter)
    
    def info(self):
        return str(self)
    
    def __str__(self): return repr(self)
    
    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join([
                repr(self.name),
                repr(self.wiki),
                repr(self.tokenizer),
                repr(self.segmenter)
            ])
        )
    
    @classmethod
    def from_config(cls, config, name):
        engine_config = config['engines'][name]
        wiki = Wiki.from_config(config, engine_config['wiki'])
        tokenizer = Tokenizer.from_config(config, engine_config['tokenizer'])
        segmenter = Segmenter.from_config(config, engine_config['segmenter'])
        return cls(
            name,
            wiki,
            tokenizer,
            segmenter
        )
