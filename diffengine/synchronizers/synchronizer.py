

class Synchronizer(Thread):
    
    def __init__(self, status, wiki, engine, tokenizer, datastore):
        
        try:
            self._init_checks(status, wiki, engine, tokenizer)
        except InitError:
            if force: logger.warn(traceback.format_exc)
            else:     raise
        
        # Store all the params
        self.status = SyncronizerStatus(status)
        self.wiki = wiki
        self.engine = engine
        self.tokenizer = tokenizer
        self.datastore = datastore
        
        # Reconfigure status
        self.status.wiki = self.wiki.id
        self.status.engine = self.engine.__class__.__name__
        self.status.tokenizer = self.tokenizer.__class__.__name__
    
    def sync_status(self):
        self.datastore.synchonizer_status.store(self.status)
        self.datastore.processor_status.sync()

    def _get_processor(self, page_id):

        try:
            processor = self.datastore.processor.get(page_id)
            logger.info("Looked up the processor for page {0} from storage.")
            logger.debug(engine_status.to_json())
            return self.engine.from_status(processor)
        except KeyError:
            logger.info("Constructing a new processor for {0}".format(page_id))
            return self.engine.new(page_id)


    def _init_checks(self, status, wiki, engine, tokenizer):
        
        # Check if we're starting up with the wrong wiki configured
        if self.status['wiki'] != self.wiki.__class__.__name__:
            raise InitError("Status 'wiki' " + \
                            "{wiki}".format(self.status) + \
                            "does not match " + \
                            "configured 'wiki' " + \
                            "{0}.".format(wiki.__class__.__name__))
        
        # Check if we're starting up with the wrong wiki engine
        if self.status['engine'] != self.engine.__class__.__name__:
            raise InitError("The status 'engine' " + \
                            "{engine}".format(self.status) + \
                            "does not match " + \
                            "configured 'engine' " + \
                            "{0}".format(engine.__class__.__name__))
        
        # Check if we're starting up with the wrong wiki tokenizer
        if self.status['tokenizer'] != self.tokenizer.__class__.__name__:
            raise InitError("The status 'tokenizer' " + \
                            "{tokenizer}".format(self.status) + \
                            "does not match " + \
                            "configured 'tokenizer' " + \
                            "{0}".format(tokenizer.__class__.__name__))
        
        # Check if we have a query_continue
        if 'query_continue' not in self.status['state']:
            raise InitError("No 'query_continue' found inside of 'state' " + \
                            "{0}".format(self.status['state']))
    
    

class LoopWaiter(Synchronizer):
    
    def __init__(self, *args, max_wait, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_wait = float(max_wait)
    
    def run(self):
        while not self._stop_requested:
            start = time.time()
            
            wait = self.synchronize()
            
            # Wait up to max_wait before performing the next synchronization
            if wait: time.sleep(self.max_wait - (time.time()-start))
            
            
            
        
    
