import logging
import traceback

from mw import api

from ..types import ProcessorStatus
from .synchronizer import Synchronizer

logger = logging.getLogger("diffengine.synchronizers.api")

class InitError(Exception): pass

def read_n(iterator, n):
    for i, value in enumerate(iterator):
        yield value
        if i+1 == n: break
    


class Changes(Synchronizer):
    
    def __init__(self, engine, source, processor_cache_size):
        
        super().__init__(engine, source)
        self.api = api.Session(wiki.api_url())
        self.changes_per_request = int(changes_per_request)
        self.max_wait = int(max_wait)
        
        # Set up the processor cache
        @lru_cache(processor_cache_size)
        def _get_cached_processor(self, page_id):
            self._get_processor(page_id)
        
        self._get_cached_processor = _get_cached_processor
        
        # Reconfigure status
        self.stats['processor_cache_size'] = processor_cache_size
        self.stats['changes_per_request'] = changes_per_request
        self.stats['max_wait'] = max_wait
        
    
    def _process_events(self, events):
        
    
    def _synchronize_revisions(self):
        
        # Get new changes
        query_continue = self.status['state'].get('query_continue')
        change_docs, query_continue = \
                self.api.recent_changes.query(query_continue=query_continue,
                                              properties={'ids'},
                                              type={'edit', 'new'})
        
        revisions_processed = 0
        
        # For each text, get the engine and update it
        for rev_doc in self._get_revisions(change_docs):
            processor = self._get_cached_processor(rev_doc['pageid'])
            text = rev_doc.get('*', "")
            
            revision = processor.process(rev_id, text)
            self.datastore.revisions.store(revision)
            self.datastore.processor_status.store(processor.status, batch=True)
            revisions_processed += 1
            self.status.stats['revisions_processed'] += 1
            self.status.stats['touched'] = time.time()
        
        self.status['state']['query_continue'] = query_continue
        return revisions_processed
    
    def _run(self):
        
        event_listener = \
                self.source.events.listen(engine_status=self.engine.status)
        
        events = deque(50)
        while not self._stop_requested:
            events = read_n(event_listener, 50)
            self._process_events(events)
            self._store_status()
            
        
    
    
    def _get_revisions(self, change_docs):
        rev_ids = [int(rc['this_old_id']) for rc in change_docs]
        
        return self.api.revisions.query(rev_ids, properties={'ids', 'content'})
