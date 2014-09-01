from .daemon import Daemon


class Synchronizer(Daemon):
    
    def __init__(self, name, synchronizers):
        super().__init__(self, name)
        self.synchronizers = list(synchronizers)
    
    def _start(self):
        for synchronizer in self.synchronizers:
            synchronizer.start()
        
    
    def _all_ok(self):
        return sum(s.isAlive() for s in self.synchronizers) == \
               len(self.synchronizers)
    
    def _graceful_stop(self):
        
        for synchronizer in synchronizers:
            synchronizer.stop()

        for synchronizer in synchronizers:
            synchronizer.wait()
        
        
    
    def status(self):
        doc = super().status()
        doc['synchronizers'] = {s.name:s.status() for s in self.synchronizers}
        
        return doc
    
    @classmethod
    def from_config(cls, config, name):
                        
        synchronizers = []
        for sync_name in config['daemons'][name]['synchronizers']:
            synchronizer = Synchronizer.from_config(config, sync_name)
            synchronizers.append(synchronizer)
            
        
        return cls(
            name,
            synchronizers
        )
