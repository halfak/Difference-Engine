

class RevisionOrderError(RuntimeError):
    
    def __init__(self, last_rev_id, rev_id):
        
        message = "Revisions out of order.  " + \
                  "Last rev ID {0}.  ".format(last_rev_id) + \
                  "Current rev ID {0}".format(rev_id)
        
        super().__init__(message)
