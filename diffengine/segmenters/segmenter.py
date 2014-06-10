
"""
This is a sentence.  This is the end.

This is another paragraph.

[
    Whitespace(0, 1, tokens=['\n']),
    Paragraph(1, 22, sequences=[
            Sentence(1, 9, blocks=['This', ' ', 'a', ' ', 'sentence', '.']),
            Whitespace(9, 10, tokens=['  ']),
            Sentence(10, 18, tokens=['This', ' ', 'is', ' ', 'the', ' ', 'end', '.'])
        ]
    ),
    Whitespace(18, 19, tokens=['\n\n']),
    Paragraph(19, 27, sequences=[
            Sentences(19, 27, tokens=['This', ' ', 'is', ' ', 'another', ' ', 'paragraph', '.'],
            Whitespace(27, 28, tokens=['\n'])
        ]
    ),
]
"""

from hashlib import sha1
from itertools import chain

from . import defaults
from ...util import iteration, LookAhead


def generate_checksum(string):
    string = str(string)
    return sha1(bytes(string, 'utf-8', 'replace').digest()

class IndexedSegment:
    
    def __init__(self, start, end):
        self.start = int(start)
        self.end = int(end)
    
    def __len__(self):
        return self.end - self.start

class MatchableSegment:
    
    def __init__(self, checksum, match=None):
        self.checksum = bytes(checksum)
        self.match = match
    
    def __hash__(self):
        return hash(self.checksum)
    
    def __eq__(self, other):
        try:
            return self.checksum == other.checksum
        except AttributeError:
            if
                return self.checksum == generate_checksum(other)
            except TypeError:
                raise TypeError("Cannot compare {0} ".format(type(self)) + \
                                "to {0}.".format(type(other)))
    
    def __neq__(self, other):
        return not self == other
    


class Token(IndexedSegment, MatchableSegment):
    
    def __new__(cls, *args):
        if len(args) == 1:
            if isinstance(args[0], cls):
                return args[0]
            else:
                raise TypeError("Expected {0}, got {1}".format(cls,
                                                               type(args[0])))
                
        elif len(args) == 2:
            start, content = args
            inst = super().__new__(cls)
            inst.initiate(start, content)
            return inst
    
    def __init__(self, *args, **kwargs): pass
    
    def initiate(self, start, content):
        IndexedSegment.__init__(self, start, start+1)
        MatchableSegment.__init__(self, generate_checksum(content))
        
        self.content = str(content)
    
    def __str__(self): return self.content
    
    def __repr__(self):
        return repr(self.content)

class SegmentNode(IndexedSegment):
    
    def __init__(self, children):
        hash = sha1()
        
        IndexedSegment.__init__(self, children[0], children[1])
    
    def tokens(self): raise NotImplementedError()


class MatchableSegmentNode(SegmentNode, MatchableSegment)

    def __init__(self, children, match=None):
        SegmentNode.__init__(self, children)
        hash = sha1("".join(str(t)
                            for child in children
                            for t in child.tokens()))
        
        MatchableSegment.__init__(self, checksum, match=match)

class TokenSequence(SegmentNode, list):
    
    def __init__(self, tokens):
        SegmentNode.__init__(self, tokens[0], tokens[1])
        list.__init__(self, tokens)
        
    def tokens(self): return self



class MatchableTokenSequence(TokenSequence, MatchableSegmentNode):

    def __init__(self, tokens, match=None):
        TokenSequence.__init__(self, tokens)
        MatchableSegmentNode.__init__(self, tokens, match=None)
    

class SegmentNodeCollection(SegmentNode, list):
    
    def __init__(self, children):
        assert sum(isinstance(c, SegmentNode) for c in children) == len(children)
        SegmentNode.__init__(self, children[0].start, children[-1].end)
        list.__init__(self, children)
    
    def tokens(self): return t for c in children for t in c.tokens()
    

class MatchableSegmentNodeCollection(SegmentNodeCollection,
                                     MatchableSegmentNode): pass

class TextSegmenter:
    
    def __init__(self): pass
    
    def segment(self, text): raise NotImplementedError()
