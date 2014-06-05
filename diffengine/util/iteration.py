from .look_ahead import LookAhead


def read_until(iterable, condition=lambda i, item: False, return_last=False):
    look_ahead = LookAhead(iterable)
    
    i = 0
    while not look_ahead.empty():
        if condition(i, look_ahead.peek()):
            if return_last: yield look_ahead.pop()
            break
        
        yield look_ahead.pop()
        
        i += 1

def read_split(tokens, match, return_last, min_match=1):
    look_ahead = LookAhead(tokens)
    
    while not look_ahead.empty():
        yield False, read_until(
            look_ahead,
            condition=lambda i, token: match.match(token) and (i+1) >= min_match,
            return_last=return_last
        )
        yield True, read_until(
            look_ahead,
            condition=lambda i, token: not match.match(token)
        )
