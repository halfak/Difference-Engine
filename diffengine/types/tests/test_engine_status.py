from nose.tools import eq_

from deltas.segmenters import ParagraphsSentencesAndWhitespace
from mw import Timestamp

from ..engine_status import EngineStatus


def test_engine_status():
    engine_info = "SequenceMatcher(Wiki(\"foo\"), WikitextSplit(), PaSW/())"
    engine_status = EngineStatus(engine_info)
    
    eq_(engine_status.engine_info, engine_info)
    eq_(engine_status.last_rev_id, 0)
    eq_(engine_status.last_timestamp, None)
    
    rev_id = 10
    timestamp = Timestamp(1234567890)
    
    engine_status.update(rev_id, timestamp)
    
    eq_(engine_status.engine_info, engine_info)
    eq_(engine_status.last_rev_id, rev_id)
    eq_(engine_status.last_timestamp, timestamp)
