from nose.tools import eq_
from mw import Timestamp
from deltas.segmenters import ParagraphsSentencesAndWhitespace

from ..sync_status import SyncContinue, APIContinue, DumpContinue, SyncStatus

def test_dump_continue():
    last_rev_id = 10
    last_timestamp = Timestamp(1234567890)
    dump_continue = DumpContinue(last_rev_id, last_timestamp)
    
    eq_(dump_continue.last_rev_id, last_rev_id)
    eq_(dump_continue.last_timestamp, last_timestamp)
    
    eq_(dump_continue, DumpContinue(dump_continue))
    eq_(dump_continue, SyncContinue(dump_continue))
    eq_(dump_continue, SyncContinue(dump_continue.to_json()))
    
    
def test_api_continue():
    query_continue = {"rccontinue": "20140722135616|670447180"}
    last_timestamp = Timestamp(1234567890)
    api_continue = APIContinue(query_continue, last_timestamp)
    
    eq_(api_continue.query_continue, query_continue)
    eq_(api_continue.last_timestamp, last_timestamp)
    
    eq_(api_continue, APIContinue(api_continue))
    eq_(api_continue, SyncContinue(api_continue))
    eq_(api_continue, SyncContinue(api_continue.to_json()))
    
    
def test_sync_status():
    name = "Herpderp"
    wiki_name = "English Wikipedia"
    engine_info = "SegmentMatcher(WikitextSplit(), ParagraphsSentencesAndWhiteSpace())"
    sync_continue = DumpContinue(10, Timestamp(1234567890))
    stats = {"foo": "bar"}
    
    sync_status = SyncStatus(name, wiki_name, engine_info, sync_continue, stats)
    
    eq_(sync_status.name, name)
    eq_(sync_status.wiki_name, wiki_name)
    eq_(sync_status.engine_info, engine_info)
    eq_(sync_status.sync_continue, sync_continue)
    eq_(sync_status.stats, stats)
    
    eq_(sync_status, SyncStatus(sync_status))
    eq_(sync_status, SyncStatus(sync_status.to_json()))
    
    
