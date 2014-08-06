from nose.tools import eq_, raises

from ...errors import RevisionOrderError
from ..processor_status import ProcessorStatus
from ..timestamp import Timestamp


def test_processor_startus():
    
    page_id = 12
    
    processor_status = ProcessorStatus(page_id)
    
    eq_(processor_status.page_id, page_id)
    
    rev_id = 3457
    timestamp = Timestamp(123567890)
    processor_status.processed(rev_id, timestamp)
    
    eq_(processor_status.last_rev_id, rev_id)
    eq_(processor_status.last_timestamp, timestamp)
    eq_(processor_status.stats['revisions_processed'], 1)
    
    eq_(processor_status, ProcessorStatus(processor_status))
    eq_(processor_status, ProcessorStatus(processor_status.to_json()))
    
def test_check_order():
    page_id = 257654
    rev_id = 3457
    timestamp = Timestamp(123567890)
    processor_status = ProcessorStatus(page_id, rev_id, timestamp)
    
    processor_status.check_order(rev_id, timestamp+1)
    processor_status.check_order(rev_id+1, timestamp)
    
@raises(RevisionOrderError)
def test_check_ordered_same():
    page_id = 257654
    rev_id = 3457
    timestamp = Timestamp(123567890)
    processor_status = ProcessorStatus(page_id, rev_id, timestamp)
    
    processor_status.processed(rev_id, timestamp)

@raises(RevisionOrderError)
def test_check_ordered_lower_rev_id():
    page_id = 257654
    rev_id = 3457
    timestamp = Timestamp(123567890)
    processor_status = ProcessorStatus(page_id, rev_id, timestamp)
    
    processor_status.processed(rev_id-1, timestamp)

@raises(RevisionOrderError)
def test_check_ordered_lower_timestamp():
    page_id = 257654
    rev_id = 3457
    timestamp = Timestamp(123567890)
    processor_status = ProcessorStatus(page_id, rev_id, timestamp)
    
    processor_status.processed(rev_id, timestamp-1)

@raises(RevisionOrderError)
def test_check_ordered_both_lower():
    page_id = 257654
    rev_id = 3457
    timestamp = Timestamp(123567890)
    processor_status = ProcessorStatus(page_id, rev_id, timestamp)
    
    processor_status.processed(rev_id-1, timestamp-1)
