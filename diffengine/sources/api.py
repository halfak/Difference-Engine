
from mw import api

from mwevents import PageCreated, RevisionSaved
from mwevents.sources import API
from mwevents.types import StateMarker

for event in listener:
    if isinstance(event, RevisionSaved):
        print(event.revision)
    else: # isinstance(event, PageCreated):
        print(event.page)

class Events:
    
    def __init__(self, session):
        
        api_source = API(session)
    
    def listener(self, engine_status):
        
        state_marker = StateMarker(last_event=engine_status.last_timestamp,
                                   last_rev_id=engine_status.last_rev_id)
        
        return api_source.listener(state_marker=state_marker,
                                   events={RevisionSaved, PageCreated})
    

class Revisions:
    
    def __init__(self, session):
        self.session = session
    
    def get(self, rev_id):
        return self.sessions.revisions.get(rev_id,
                                           properties={'ids', 'timestamp',
                                                       'user', 'userid',
                                                       'content'})
    
    def all_for_page(self, page_id, up_to_rev_id):
        return self.sessions.revisions.query(pageids={page_id},
                                             properties={'ids', 'timestamp',
                                                         'user', 'userid',
                                                         'content'})
