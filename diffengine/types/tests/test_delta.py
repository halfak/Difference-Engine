from nose.tools import eq_

from ..delta import Delta
from ..operations import Delete, Equal, Insert


def test_delta():
    chars = 2545
    bytes = 5838
    operations = [Insert(0,1,0,1,["foo"]), Delete(1,2,1,1, ["bar"]), Equal(2,100,1,99)]
    delta = Delta(bytes, chars, operations)
    
    eq_(delta.bytes, bytes)
    eq_(delta.chars, chars)
    eq_(delta.operations, operations)
    
    eq_(delta, Delta(delta))
    eq_(delta, Delta(delta.to_json()))
