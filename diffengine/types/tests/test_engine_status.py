from nose.tools import eq_

from ..engine_status import EngineStatus
from ..timestamp import Timestamp

def test_engine_status():
    
    page_id = 12
    
    engine_status = EngineStatus(page_id)
    
    eq_(engine_status.page_id, page_id)
    
    rev_id = 3457
    timestamp = Timestamp(123567890)
    engine_status.update(rev_id, timestamp)
    
    eq_(engine_status.last_rev_id, 3457)
    eq_(engine_status.last_timestamp, timestamp)
    eq_(engine_status.stats['revisions_processed'], 1)
    
    eq_(engine_status, EngineStatus(engine_status))
    eq_(engine_status, EngineStatus(engine_status.to_json()))
