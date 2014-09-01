from .daemon import Daemon


class WebserverAndSynchronizer(Daemon):
    
    def __init__(self, name, webserver, synchronizers):
        super().__init__(self, name)
        self.synchronizer = synchronizer
        self.webserver = webserver
    
    def _start(self):
        self.synchronizer._start()
        self.webserver._start()
    
    def _all_ok(self):
        return self.synchronizer._all_ok() and \
               self.webserver._all_ok()
    
    def _graceful_stop(self):
        return self.synchronizer._graceful_stop() and \
               self.webserver._graceful_stop()
    
    def status(self):
        doc = self.synchronizer.status()
        doc.update(self.webserver.status())
        
        return doc
    
    @classmethod
    def from_config(cls, config, name):
        
        cls(
            name,
            Synchronizer.from_config(config, name),
            Webserver.from_config(config, name)
        )
