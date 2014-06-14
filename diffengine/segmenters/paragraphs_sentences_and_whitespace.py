import re
from .segmenter import TextSegmenter, Token, MatchableSegmentNodeCollection, \
                       MatchableTokenSequence, TokenSequence
from ..util import LookAhead

class Paragraph(MatchableSegmentNodeCollection):pass
class Sentence(MatchableTokenSequence):pass
class Whitespace(TokenSequence):pass

class ParagraphsSentencesAndWhitespace(TextSegmenter):
    
    def __init__(self, whitespace, paragraph_split, sentence_end, *,
                       min_sentence=6):
        
        
        if not hasattr(whitespace, "match"):
            raise TypeError("whitespace is the wrong type." + \
                            "Expected {0}, ".format(type(re.compile(" "))) + \
                            "got {0}".format(type(whitespace)))
        self.whitespace = whitespace
        
        if not hasattr(paragraph_split, "match"):
            raise TypeError("paragraph_split is the wrong type." + \
                            "Expected {0}, ".format(type(re.compile(" "))) + \
                            "got {0}".format(type(paragraph_split)))
        self.paragraph_split = paragraph_split
                
        
        if not hasattr(sentence_end, "match"):
            raise TypeError("sentence_end is the wrong type." + \
                            "Expected {0}, ".format(type(re.compile(" "))) + \
                            "got {0}".format(type(sentence_end)))
        self.sentence_end = sentence_end
        
        self.min_sentence = int(min_sentence)
    
    def segment(self, tokens):
        
        self.look_ahead = LookAhead(tokens)

        segments = []

        while not self.look_ahead.empty():
            if self.whitespace.match(self.look_ahead.peek()):
                segment = self._read_whitespace(self.look_ahead)
            else:
                segment = self._read_paragraph(self.look_ahead)
                
            segments.append(segment)

        return segments
    
    def _read_whitespace(self, look_ahead):
        #print("Reading whitespace.")
        
        whitespace_tokens = []
        
        while not look_ahead.empty() and \
              self.whitespace.match(self.look_ahead.peek()):
            whitespace_tokens.append(Token(look_ahead.i, look_ahead.pop()))
            
        
        return Whitespace(whitespace_tokens)
    
    def _read_sentence(self, look_ahead):
        #print("Reading sentence.")
        
        sentence_tokens = []
        
        while not look_ahead.empty() and \
              not self.paragraph_split.match(look_ahead.peek()):
            
            sentence_bit = look_ahead.pop()
            sentence_tokens.append(Token(look_ahead.i, sentence_bit))
            
            if self.sentence_end.match(sentence_bit) and \
               len(sentence_tokens) >= self.min_sentence:
                break
            
        return Sentence(sentence_tokens)
    
    def _read_paragraph(self, look_ahead):
        #print("Reading paragraph.")
        
        segments = []
        
        while not look_ahead.empty() and \
              not self.paragraph_split.match(look_ahead.peek()):
            
            if self.whitespace.match(look_ahead.peek()):
                segment = self._read_whitespace(look_ahead)
            else:
                segment = self._read_sentence(look_ahead)
                
            segments.append(segment)
        
        return Paragraph(segments)
    
