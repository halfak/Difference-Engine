
from mw.api import Session


class APISource:
    
    def __init__(self, url, sync_status=None):
        
        self.session = Session(url)
        self.set_status(sync_status)
    
    def set_status(self, sync_status)
        self.sync_status = sync_status
    
    def read(self, max_wait):
        
        if self.sync_status == None:
            logger.warning("Starting synchronization with no status.  " +
                           "Will start from the beginning.")
            rccontinue = None
            start = None
        
        elif hasattr(self.sync_status, "rccontinue"):
            rccontinue = self.sync_status.rccontinue()
            start = None
        
        else:
            rccontinue = None
            start = self.sync_status.last_timestamp()
        
        change_docs, rccontinue = self.session.recent_changes._query(
                direction = "newer",
                start = start
                rccontinue = rccontinue,
                types={'edit', 'new', 'external'},
                properties={'ids', 'timestamp'}
        )
        for change_doc in change_docs:
