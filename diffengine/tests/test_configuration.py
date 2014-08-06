from nose.tools import eq_

from .. import configuration


def test_propagate_defaults():
    input = {
        'foos': {
            'defaults': {
                'herp': 0,
                'derp': 0
            },
            'bar': {
                'herp': 1
            },
            'foo': {
            }
        }
    }
    expected = {
        'foos': {
            'defaults': {
                'herp': 0,
                'derp': 0
            },
            'bar': {
                'herp': 1,
                'derp': 0
            },
            'foo': {
                'herp': 0,
                'derp': 0
            }
        }
    }
    doc = configuration.propagate_defaults(input)
    
    eq_(doc, expected)
