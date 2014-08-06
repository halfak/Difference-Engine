


class RevisionOrderError(RuntimeError):
    
    def __init__(self, last_rev, rev):
        
        message = "Revisions out of order.  " + \
                  "Last rev {0}.  ".format(last_rev) + \
                  "Current rev {0}.  ".format(rev)
        
        super().__init__(message)


class ChangeWarning(Warning):
    """
    Represents a change to a portion of configuration that is not expected to
    change.  This should result in a warning and a confirmation from the user
    to force the issue.
    """
