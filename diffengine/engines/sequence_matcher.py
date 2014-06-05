from difference import sequence_matcher


class SequenceMatcher(DifferenceEngine):
    
    def __init__(self, last=None):
        self.last = last if last != None else []
    
    def process(self, tokens):
        delta = sequence_matcher.diff(self.last, tokens)
        
        return delta
        
    def serialize(self):
        return {'list': list(self.last)}
    
    @classmethod
    def deserialize(cls, doc):
        return cls(last=doc['last'])
