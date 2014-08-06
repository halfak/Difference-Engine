from nose.tools import eq_

from .. import instance


def test_simple_repr():
    
    eq_(
        instance.simple_repr("Classname", 'foo', 5, herp=[5]),
        "Classname('foo', 5, herp=[5])"
    )
