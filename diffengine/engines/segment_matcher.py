from deltas import segment_matcher, Segmenter

from ..errors import RevisionOrderError
from ..types import Delta, EngineStatus, Operation, ProcessorStatus
from .engine import Engine, Processor


class SegmentMatcherProcessorStatus(ProcessorStatus):
    
    def initiate(self, page_id, last_rev_id=0, last_tokens=None, **kwargs):
        super().initiate(page_id, last_rev_id, **kwargs)
        
        self.last_tokens = last_tokens or []
    
    def processed(self, rev_id, timestamp, tokens):
        self.set_state(rev_id, timestamp, tokens)
        self._increment_revisions()
    
    def set_state(self, last_rev_id, last_timestamp, last_tokens, **stats):
        super().set_state(last_rev_id, last_timestamp, **stats)
        self.last_tokens = last_tokens
    

class SegmentMatcherProcessor(Processor):
    
    STATUS = SegmentMatcherProcessorStatus
    
    def __init__(self, status, tokenizer, segmenter):
        
        self.status = SegmentMatcherProcessorStatus(status)
        
        self.tokenizer = tokenizer
        self.segmenter = segmenter
        
        self.last_text = "".join(self.status.last_tokens)
    
    def process(self, rev_id, timestamp, text):
        if rev_id < self.status.last_rev_id:
            raise RevisionOrderError(self.status.last_rev_id, rev_id)
        
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

class SegmentMatcher(Engine):
    
    PROCESSOR = SegmentMatcherProcessor
    
    def __init__(self, wiki, store, tokenizer, segmenter, force=False):
        super().__init__(wiki, store)
        self.tokenizer = tokenizer
        self.segmenter = segmenter
        
        status = self.store.get_status()
        
        if status == None:
            if force:
                status = EngineStatus(self.info)
            else:
                raise ChangeWarning("No engine status found.\n" + \
                                    " - configured: {0}\n".format(self.info()))
        
        if self.info() != status.engine_info:
            if force:
                status.engine_info = self.info()
            else:
                raise ChangeWarning(
                        "Stored engine status does " + \
                        "not match configuration.\n" + \
                        " - stored: {0}\n".format(status.engine_info) + \
                        " - configured: {0}\n".format(self.info()))
            
        self.status = status
        
    
    def info(self):
        return str(self)
    
    def __str__(self): return repr(self)
    
    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join([
                repr(self.wiki),
                repr(self.store),
                repr(self.tokenizer),
                repr(self.segmenter)
            ])
        )
