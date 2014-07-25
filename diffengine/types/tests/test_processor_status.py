from nose.tools import eq_

from ..processor_status import ProcessorStatus
from ..timestamp import Timestamp


def test_processor_startus():
    
    page_id = 12
    
    processor_startus = ProcessorStatus(page_id)
    
    eq_(processor_startus.page_id, page_id)
    
    rev_id = 3457
    timestamp = Timestamp(123567890)
    processor_startus.processed(rev_id, timestamp)
    
    eq_(processor_startus.last_rev_id, 3457)
    eq_(processor_startus.last_timestamp, timestamp)
    eq_(processor_startus.stats['revisions_processed'], 1)
    
    eq_(processor_startus, ProcessorStatus(processor_startus))
    eq_(processor_startus, ProcessorStatus(processor_startus.to_json()))
