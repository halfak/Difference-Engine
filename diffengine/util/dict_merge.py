

def dict_merge(d1, d2):
    """
    Recursively merges values from d2 into d1.
    """
    for key in d2:
        if key in d1 and isinstance(d1[key], dict) and isinstance(d2[key], dict):
                dict_merge(d1[key], d2[key])
        else:
            d1[key] = d2[key]
        
    
    return d1
