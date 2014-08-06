import copy
import importlib

import yaml

from .util import dict_merge


def propagate_defaults(config_doc):
    for group_name, group_doc  in config_doc.items():
        if isinstance(group_doc, dict):
            defaults = group_doc.get('defaults', {})
            
            for item_name, item_doc in group_doc.items():
                if item_name == 'defaults': continue
                if isinstance(item_doc, dict):
                    
                    group_doc[item_name] = dict_merge(copy.deepcopy(defaults),
                                                      item_doc)
                    
        
    
    return config_doc

def import_class(path):
    path = str(path)
    modules = path.split(".")
    
    if len(modules) == 1:
        return importlib.import_module(modules[0])
    else:
        module = importlib.import_module(".".join(modules[:-1]))
        try:
            return getattr(module, modules[-1])
        except AttributeError as e:
            raise ImportError("Cannot import path {0}  ".format(path) + str(e))
            
        
    


def from_file(f):
    
    doc = yaml.load(f)
    
    return propagate_defaults(doc)
