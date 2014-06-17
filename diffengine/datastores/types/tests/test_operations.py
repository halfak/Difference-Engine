from nose.tools import eq_

from ..operations import Operation, OperationWithTokens, Insert, Persist, Remove

def test_operation_with_tokens():
    start = 0
    end = 3
    tokens = ['one', 'two', 'three']
    insert = Insert(start, end, tokens)
    assert isinstance(insert, Operation)
    assert isinstance(insert, OperationWithTokens)

    eq_(insert.start, start)
    eq_(insert.end, end)
    eq_(insert.tokens, tokens)

    eq_(insert, OperationWithTokens(insert.to_json()))
