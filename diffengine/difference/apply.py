from .ops import Insert, Persist, Remove


def apply(ops, a_tokens, b_tokens):
    
    for op in ops:
        
        if isinstance(op, Persist):
            yield from a_tokens[op.start:op.end]
        
        elif isinstance(op, Insert):
            yield from b_tokens[op.start:op.end]
        
        else: #isinstance(op, Remove):
            pass
