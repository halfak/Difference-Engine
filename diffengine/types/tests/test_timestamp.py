from nose.tools import eq_

from ..timestamp import Timestamp

def test_timestamp():
    
    timestamp = Timestamp(1234567890)
    
    eq_(timestamp, Timestamp(timestamp))
    eq_(timestamp, Timestamp(timestamp.to_json()))
