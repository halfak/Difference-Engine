import yaml, importlib



def propagate_defaults(doc):
    for key, sub_doc  in doc.items():
        if isinstance(sub_doc, dict):
            defaults = sub_doc.get('defaults', {})
            
            for sub_key, sub_sub_doc in sub_doc.items():
                
                if isinstance(sub_sub_doc, dict):
                    merge_config(sub_sub_doc, defaults)
        
    
    return doc


def merge_config(d, defaults):
    
    for key in defaults:
        if key in d:
            if isinstance(d[key], dict):
                merge_config(d[key], defaults[key])
        else:
            d[key] = defaults[key]
        
    

def from_path(path):
    return from_file(open(path))

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
