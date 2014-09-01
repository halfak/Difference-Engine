
from mw import api


class APIEvents:
    
    def __init__(self, api_url):
        
        self.api_session = api.Session(api_url)
        self.set_status(sync_status)
    
    def listen(self, start):
        
        change_docs, rccontinue = self.session.recent_changes._query(
                direction = "newer",
                start = start,
                rccontinue = rccontinue,
                types={'edit', 'new', 'external'},
                properties={'ids', 'timestamp'}
        )
        for change_doc in change_docs:
            pass
    
    def _read_changes(self, rccontinue):
        pass
