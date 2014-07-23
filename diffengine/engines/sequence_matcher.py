from deltas import sequence_matcher


class SegmentMatcherEngine(DifferenceEngine):
    
    def __init__(self, status, tokenizer):
        self.status    = status
        self.tokenizer = tokenizer
        
        self.last_text = "".join(self.status.last_tokens)
    
    def process(self, rev_id, timestamp, new_text):
        if rev_id < self.status.last_rev_id:
            raise RevisionOrderError(self.status.last_rev_id, rev_id)
        
        new_tokens = self.tokenizer.tokenize(new_text)
        
        deltas_ops = sequence_matcher.diff(self.status.last_tokens, new_tokens)
        operations = list(
                Operation.from_delta_op(op, self.status.last_tokens, new_tokens)) \
                for op in deltas_ops
        )
        
        chars = len(new_text) - len(self.last_text)
        bytes = len(bytes(new_text, 'utf-8', 'replace')) -
                len(bytes(self.last_text, 'utf-8', 'replace'))
        
        delta = Delta(sequence_matcher.__name__, chars, bytes, operations)
        
        self.status.update(rev_id, timestamp)
        self.last_text = new_text
