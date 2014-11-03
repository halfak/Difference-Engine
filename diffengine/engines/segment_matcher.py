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
    
    def __init__(self, status, engine):
        super().__init__(status)
        self.engine = engine
    
    def set_status(self, status):
        self.status = SegmentMatcherProcessorStatus(status)
    
    def process(self, rev_id, timestamp, text):
        self.status.check_order(rev_id, timestamp)
        
        tokens = self.engine.tokenizer.tokenize(text)
        
        delta = self.engine.diff(self.status.last_tokens, tokens)
        
        self.status.processed(rev_id, timestamp, tokens)
        
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
        return self.Processor(status, self)
    
    def diff(self, last, current):
        if isinstance(last, str): last = self.tokenizer.tokenize(last)
        if isinstance(current, str): current = self.tokenizer.tokenize(current)
        
        deltas_ops = segment_matcher.diff(
            last,
            current,
            segmenter = self.segmenter
        )
        operations = [Operation.from_delta_op(op, last, current)
                      for op in deltas_ops]
        
        char_diff = len("".join(current)) - len("".join(last))
        byte_diff = len(bytes("".join(current), 'utf-8', 'replace')) - \
                    len(bytes("".join(last), 'utf-8', 'replace'))
        
        return Delta(char_diff, byte_diff, operations)
    
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
