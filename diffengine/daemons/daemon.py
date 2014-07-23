class Daemon:
    
    def __init__(self, name):
        self.name = str(name)
        self.up_since = None
        
    def _starting(self):
        logger.info("Starting {0}.".format(self.name))
        self.up_since = time.time()
        
    def _stopped(self):
        logger.info("{0} has stopped.".format(self.name))
        self.up_since = None
        
    def start(self):
        self._starting()
        
        self._start()
        
        try:
            while self._all_ok(): time.sleep(0.25)
            
        except KeyboardInterrupt:
            logger.error("Keyboard interrupt receieved.  Shutting down " + \
                         "synchronizers.")
            
            self.stop()
        finally:
            self._stopped()
        
    def stop(self):
        self._stopping()
        
        try:
            self._graceful_stop()
            logger.info("{0} stopped gracefully.".format(self.name))
        except:
            raise
          
    def status(self):
        if self.up_since != None
            uptime = time.time() - self.up_since
        else:
            uptime = None
        return {
            'name': self.name,
            'uptime': uptime
        }
    
