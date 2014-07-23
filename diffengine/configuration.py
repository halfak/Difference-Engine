import yaml, importlib, copy

from .util import dict_merge

def propagate_defaults(config_doc):
    for key, sub_doc  in doc.items():
        if isinstance(sub_doc, dict):
            defaults = sub_doc.get('defaults', {})
            
            for sub_key, sub_sub_doc in sub_doc.items():
                
                if isinstance(sub_sub_doc, dict):
                    
                    sub_doc[sub_key] = dict_merge(copy.deepcopy(defaults),
                                                  sub_sub_doc)
                    
        
    
    return config_doc

def import_class(path):
        modules = path.split(".")
        
        try:
                if len(modules) == 1:
                        return importlib.import_module(modules[0])
                else:
                        module = importlib.import_module(".".join(modules[:-1]))
                        return getattr(module, modules[-1])
        
        except ImportError as e:
                raise ImportError(str(e) + "(%s)" % path)

def from_file(f):
    
    doc = yaml.load(f)
    
    return propagate_defaults(doc)
