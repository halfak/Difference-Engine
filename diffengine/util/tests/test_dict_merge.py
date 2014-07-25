from nose.tools import eq_

from ..dict_merge import dict_merge

def test_dict_merge():
    
    d1 = {
        'foo': {
            'bar': {
                'val0': 100,
                'val1': 5
            },
            'herp': 5
        },
        'herpderp': "yup"
    }
    
    d2 = {
        'bar': 5,
        'foo': {
            'bar': {
                'val1': 10,
                'val2': 11
            },
            'herp': {'derp': 10}
        }
    }
    
    expected = {
        'bar': 5,
        'foo': {
            'bar': {
                'val0': 100,
                'val1': 10,
                'val2': 11
            },
            'herp': {'derp': 10}
        },
        'herpderp': "yup"
    }
    
    dict_merge(d1, d2)
    
    eq_(d1, expected)
