from deltas import apply
from deltas.segmenters import ParagraphsSentencesAndWhitespace
from nose.tools import eq_, raises

from ...errors import RevisionOrderError
from ...tokenizers import WikitextSplit
from ...types import ProcessorStatus, Timestamp
from ..segment_matcher import (SegmentMatcher, SegmentMatcherProcessor,
                               SegmentMatcherProcessorStatus)


def test_segment_matcher_processor():
    
    status = SegmentMatcherProcessorStatus(12)
    processor = SegmentMatcherProcessor(status,
                          WikitextSplit(), ParagraphsSentencesAndWhitespace())
    
    rev_id = 34567
    timestamp = Timestamp(1234567890)
    new_text_1 = "This is new text"
    delta = processor.process(rev_id, timestamp, new_text_1)
    
    eq_(delta.bytes, len(bytes(new_text_1, 'utf-8')))
    eq_(delta.chars, len(new_text_1))
    eq_(len(delta.operations), 1)
    
    rev_id = 457890
    timestamp = Timestamp(1234567891)
    new_text_2 = "This is newer text"
    delta = processor.process(rev_id, timestamp, new_text_2)
    
    eq_(delta.chars, 2)
    eq_(delta.bytes, 2)
    eq_(len(delta.operations), 4)
    
    a_tokens = WikitextSplit().tokenize(new_text_1)
    b_tokens = WikitextSplit().tokenize(new_text_2)
    
    eq_(
        b_tokens,
        list(apply([op.to_delta_op() for op in delta.operations], a_tokens, b_tokens))
    )


def test_revision_out_of_order():
    
    status = SegmentMatcherProcessorStatus(12)
    processor = SegmentMatcherProcessor(status,
                          WikitextSplit(), ParagraphsSentencesAndWhitespace())
    
    delta = processor.process(
        1001,
        Timestamp(1234567890),
        "This is new text"
    )
    try:
        delta = processor.process(
            1000,
            Timestamp(1234567890),
            "This is new text"
        )
    except RevisionOrderError:
        delta = processor.process(
            1002,
            Timestamp(1234567891),
            "This is new text"
        )
    else:
        assert False, "Should have thrown a RevisionOrderError"
