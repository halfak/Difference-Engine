from mw.xml_dump import map

class XMLDump(Synchronizer):
    
    def __init__(self, sync_status, wiki, engine, datastore,
                       paths, threads, force=False):
        
        super().__init__(sync_status, wiki, engine, datastore)
        
        self.sync_status.stats['touched'] = time.time()
        
    
    def run(self):
        
        max_rev_id = None
        max_timestamp = None
        
        for processor_revision_or_dump in map(paths, self._process_dump):
            
            if isinstance(revision_processor_or_dump, Revision):
                revision = revision_processor_or_dump
                
                self.datastore.revisions.store(revision)
                self.status.stats['revisions_processed'] += 1
                
                max_rev_id = max(revision.rev_id, max_rev_id or 0)
                max_timestamp = max(revision.timestamp, max_timestamp or 0)
                
            elif isinstance(revision_processor_or_dump, Processor):
                processor = revision_processor_or_dump
                
                self.datastore.processor.store(processor)
                
                logging.info("Completed processing page " + \
                             "{0}".format(processor_status.page_id))
                
            elif isinstance(revision_processor_or_dump, xml_dump.Iterator):
                dump = revision_processor_or_dump
                
                logging.info("Completed processing dump {0}".format(dump.path))
                
            else:
                raise RuntimeError(
                        "Did not expect a " + \
                        "{0}".format(type(revision_processor_or_dump)))
        
        self.sync_status.last_rev_id = rev_id
        
        self.store_status()
    
    
    def _process_dump(self, dump):
        
        for page in dump:
            processor = self._get_processor(page.id)
            
            for rev in page: # For processor in page
                if rev.id >= processor.last_id:
                    revision = processor.process(rev.text)
                    self.datastore.revisions.store(revision)
                    yield revision
                    
                
            
            yield processor
        
        yield dump
        
        
