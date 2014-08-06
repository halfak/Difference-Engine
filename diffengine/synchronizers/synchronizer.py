import logging
from threading import Thread

from ..errors import ChangeWarning

logger = logging.getLogger("diffengine.synchronizers.synchronizer")

class Synchronizer(Thread):
    
    def __init__(self, engine, store, force_config=False):
        super().__init__()
        
        # Store all the params
        self.engine = engine
        self.store = store
        
        status = self.store.engine_status.get(type=self.engine.Status)
        
        if status == None:
            if force_config:
                logger.info("Starting new Engine. " + \
                            " - configured: {0}".format(self.engine.info()))
                status = self.engine.Status(self.engine.info())
            else:
                raise ChangeWarning("No engine status found.\n" + \
                                    " - configured: {0}\n".format(self.engine.info()))
        
        if self.engine.info() != status.engine_info:
            if force_config:
                logger.warning("Overwriting engine status with " + \
                               "new configuration.\n" + \
                               " - stored: {0}\n".format(status.engine_info) + \
                               " - configured: {0}".format(self.engine.info()))
                status.engine_info = self.engine.info()
            else:
                raise ChangeWarning(
                        "Stored engine status does " + \
                        "not match configuration.\n" + \
                        " - stored: {0}\n".format(status.engine_info) + \
                        " - configured: {0}".format(self.engine.info()))
            
        self.status = status
        

    def _get_processor(self, page_id):
        page_id = int(page_id)
        processor_status = self.store.processor_status.get(page_id)
        if processor_status is None:
            logger.debug("Constructing a new processor for {0}".format(page_id))
            return self.engine.processor(self.engine.Processor.Status(page_id))
        else:
            logger.debug("Constructing a new process from " + \
                         "{0}".format(processor_status))
            return self.engine.processor(processor_status)

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
