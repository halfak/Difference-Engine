import inspect
from itertools import chain


def simple_repr(class_name, *args, **kwargs):
    class_name = str(class_name)
    arguments = [repr(arg) for arg in args]
    arguments.extend("{0}={1}".format(k, repr(v)) for k, v in kwargs.items())
    
    return "{0}({1})".format(class_name, ", ".join(arguments))

def kwargs_slots_repr(instance):
    
    return simple_repr(instance.__class__.__name__, **dict(items(instance)))

def items(instance):
    for key in keys(instance):
        yield key, getattr(instance, key)

def keys(instance):
    cls = instance.__class__
    
    return set(chain(*(getattr(cls, '__slots__', [])
                     for cls in instance.__class__.__mro__)))
