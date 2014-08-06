import copy
import logging
import re

import deltas.segmenters

from ..util import instance
from .segmenter import Segmenter

logger = logging.getLogger("diffengine.stores.paragraphs_sentence_and_whitespace")


class ParagraphsSentencesAndWhitespace(\
        deltas.segmenters.ParagraphsSentencesAndWhitespace,
        Segmenter):
    
    @classmethod
    def from_config(cls, config, name):
        psw_config = config['segmenters'][name]
        
        
        return cls(
            whitespace=re.compile(psw_config['whitespace']),
            paragraph_split=re.compile(psw_config['paragraph_split']),
            sentence_end=re.compile(psw_config['sentence_end']),
            min_sentence=psw_config['min_sentence']
        )
    
    def __repr__(self):
        return instance.simple_repr(self.__class__.__name__,
                                    whitespace=self.whitespace.pattern,
                                    paragraph_split=self.paragraph_split.pattern,
                                    sentence_end=self.sentence_end.pattern,
                                    min_sentence=self.min_sentence)
