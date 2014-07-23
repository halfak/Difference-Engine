from nose.tools import eq_
from deltas.segmenters import ParagraphsSentencesAndWhitespace
from deltas import apply

from ...types import EngineStatus, Timestamp
from ...tokenizers import WikitextSplit
from ..segment_matcher import SegmentMatcher, SegmentMatcherStatus

def test_segment_matcher():
    
    status = SegmentMatcherStatus(12)
    segment_matcher = SegmentMatcher(WikitextSplit(),
                                     ParagraphsSentencesAndWhitespace(),
                                     status)
    
    rev_id = 34567
    timestamp = Timestamp(1234567890)
    new_text_1 = "This is new text"
    delta = segment_matcher.process(rev_id, timestamp, new_text_1)
    
    eq_(delta.bytes, len(bytes(new_text_1, 'utf-8')))
    eq_(delta.chars, len(new_text_1))
    eq_(len(delta.operations), 1)
    
    rev_id = 457890
    timestamp = Timestamp(1234567891)
    new_text_2 = "This is newer text"
    delta = segment_matcher.process(rev_id, timestamp, new_text_2)
    
    eq_(delta.chars, 2)
    eq_(delta.bytes, 2)
    eq_(len(delta.operations), 4)
    
    a_tokens = WikitextSplit().tokenize(new_text_1)
    b_tokens = WikitextSplit().tokenize(new_text_2)
    
    eq_(
        b_tokens,
        list(apply([op.to_delta_op() for op in delta.operations], a_tokens, b_tokens))
    )
    
    
