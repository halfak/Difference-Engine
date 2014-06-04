from hashlib import sha1

from . import defaults
from ...util import LookAhead

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


class TokenCluster:
    
    def __init__(self, start, end, checksum, matches=None):
        self.start = int(start)
        self.end = int(end)
        self.checksum = str(checksum)
        self.matches = matches or []
        
    def add_match(self, token_cluster):
        self.matches.append(token_cluster)
    
    def matched(self):
        return len(self.matches) > 0
    
    def __hash__(self):
        return hash(self.checksum)
    
    def __eq__(self, other):
        try:
            return self.checksum == other.checksum
        except AttributeError:
            raise TypeError("Cannot compare {0} to {1}.".format(type(self),
                                                                type(other)))
    
    def __neq__(self, other):
        return not self == other
    
    def __len__(self):
        return self.end - self.start



class Token(TokenCluster):
    
    def __init__(self, start, content, matches=None):
        self.content = str(content)
        checksum = hash = sha1(bytes(content, 'utf8')).digest()
        super().__init__(start, start+1, checksum, matches=matches)
    
    
    def tokens(self): return iter([self])
    
    def __repr__(self):
        return repr(self.content)

class TokenSequence(TokenCluster, list):
    
    def __init__(self, start, end, tokens, matches=None):
        hash = sha1()
        for token in tokens:
            hash.update(bytes(token.content, 'utf8'))
        
        TokenCluster.__init__(self, start, end, hash.digest(), matches=matches)
        list.__init__(self, tokens)
    
    def tokens(self): return iter(self)
    
    def __repr__(self):
        return "{0}({1}, {2}, {3}, {4})".format(
            self.__class__.__name__,
            repr(self.start),
            repr(self.end),
            "matches={0}".format(repr(self.matches)),
            list.__repr__(self)
        )


class SequenceCollection(TokenCluster, list):
    
    def __init__(self, start, end, sequences, matches=None):
        
        hash = sha1()
        for sequence in sequences:
            for token in sequence:
                hash.update(bytes(token.content, 'utf8'))
            
        
        TokenCluster.__init__(self, start, end, hash.digest(), matches=matches)
        list.__init__(self, sequences)
    
    def tokens(self): return (t for t in s for s in self)
    
    def __repr__(self):
        return "{0}({1}, {2}, {3}, {4})".format(
            self.__class__.__name__,
            repr(self.start),
            repr(self.end),
            "matches={0}".format(repr(self.matches)),
            list.__repr__(self)
        )

class Paragraph(SequenceCollection):pass
class Sentence(TokenSequence):pass
class Whitespace(TokenSequence):pass

def read_whitespace(look_ahead, tokenizer, offset):
    #print("Reading whitespace.")
    
    whitespace_offset = offset
    whitespace_tokens = []
    
    while not look_ahead.empty() and tokenizer.WHITESPACE.match(look_ahead.peek()):
        whitespace_tokens.append(Token(offset, look_ahead.pop()))
        offset += 1
        
    
    assert len(whitespace_tokens) == offset - whitespace_offset
    return Whitespace(whitespace_offset, offset, whitespace_tokens)

def read_sentence(look_ahead, tokenizer, offset, min_size):
    #print("Reading sentence.")
    
    sentence_offset = offset
    sentence_tokens = []
    while not look_ahead.empty() and \
          not tokenizer.PARAGRAPH_SPLIT.match(look_ahead.peek()):
        
        sentence_bit = look_ahead.pop()
        sentence_tokens.append(Token(offset, sentence_bit))
        offset += 1
        
        if tokenizer.SENTENCE_END.match(sentence_bit) and \
           offset - sentence_offset >= min_size:
            break
        
    assert len(sentence_tokens) == offset - sentence_offset
    return Sentence(sentence_offset, offset, sentence_tokens)

def read_paragraph(look_ahead, tokenizer, offset, min_size):
    #print("Reading paragraph.")
    
    paragraph_offset = offset
    paragraph_sequences = []
    while not look_ahead.empty() and \
          not tokenizer.PARAGRAPH_SPLIT.match(look_ahead.peek()):
        
        if tokenizer.WHITESPACE.match(look_ahead.peek()):
            sequence = read_whitespace(look_ahead, tokenizer, offset)
        else:
            sequence = read_sentence(look_ahead, tokenizer, offset, min_size)
            
        offset = sequence.end
        paragraph_sequences.append(sequence)
    
    return Paragraph(paragraph_offset, offset, paragraph_sequences)


def cluster(tokens, tokenizer, min_size=defaults.MIN_GROUP_SIZE):

    look_ahead = LookAhead(tokens)
    offset = 0
    
    clusters = []
    
    while not look_ahead.empty():
        if tokenizer.WHITESPACE.match(look_ahead.peek()):
            token_cluster = read_whitespace(look_ahead, tokenizer, offset)
        else:
            token_cluster = read_paragraph(look_ahead, tokenizer, offset, min_size)
        
        clusters.append(token_cluster)
        offset = token_cluster.end
    
    return clusters
