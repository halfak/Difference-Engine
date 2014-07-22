import inspect
from itertools import chain

def repr(instance):
    return "%s(%s)" % (
        instance.__class__.__name__,
        ", ".join(
            "%s=%r" % (k, v) for k, v in items(instance)
        )
    )

def items(instance):
    for key in keys(instance):
        yield key, getattr(instance, key)

def keys(instance):
    cls = instance.__class__
    
    return set(chain(*(getattr(cls, '__slots__', [])
                     for cls in instance.__class__.__mro__)))
