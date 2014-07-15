from nose.tools import eq_

from ..operations import Operation, OperationWithTokens, Insert, Equal, Delete

def test_operation_with_tokens():
    a1 = 0
    a2 = 3
    b1 = 10
    b2 = 13
    tokens = ['one', 'two', 'three']
    insert = Insert(a1, a2, b1, b2, tokens)
    assert isinstance(insert, Operation)
    assert isinstance(insert, OperationWithTokens)
    
    print(insert)
    eq_(insert.a1, a1)
    eq_(insert.a2, a2)
    eq_(insert.b1, b1)
    eq_(insert.b2, b2)
    eq_(insert.tokens, tokens)

    eq_(insert, OperationWithTokens(insert.to_json()))
