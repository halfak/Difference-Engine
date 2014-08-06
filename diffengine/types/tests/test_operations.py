from nose.tools import eq_

from ..operations import Delete, Equal, Insert, Operation


def test_operation():
    a1 = 0
    a2 = 3
    b1 = 10
    b2 = 13
    
    equal = Equal(a1, a2, b1, b2)
    assert isinstance(equal, Operation)
    
    eq_(equal.a1, a1)
    eq_(equal.a2, a2)
    eq_(equal.b1, b1)
    eq_(equal.b2, b2)
    
    eq_(equal, Operation(equal.to_json()))

def test_operation_with_tokens():
    a1 = 0
    a2 = 3
    b1 = 10
    b2 = 13
    tokens = ['one', 'two', 'three']
    insert = Insert(a1, a2, b1, b2, tokens)
    assert isinstance(insert, Operation)
    
    
    eq_(insert.a1, a1)
    eq_(insert.a2, a2)
    eq_(insert.b1, b1)
    eq_(insert.b2, b2)
    eq_(insert.tokens, tokens)
    
    eq_(insert, Operation(insert.to_json()))
