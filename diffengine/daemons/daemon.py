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


class SyncAndWeb(Server):
    
    def __init__(self, name, sync, web):
        super().__init__(self, name)
        self.sync = sync
        self.web = web
    
    def _start(self):
        self.sync._start()
        self.web._start()
    
    def _all_ok(self):
        return self.sync._all_ok() and self.web._all_ok()
    
    def _graceful_stop(self):
        return self.sync._graceful_stop() and self.web._graceful_stop()
    
    def status(self):
        doc = self.sync.status()
        doc.update(self.web.status())
        
        return doc
    
    @classmethod
    def from_config(cls, config, key):
        
        datastore = Datastore.from_config(config,
                                          config['servers'][key]['datastore'])
        
        cls(
            config['servers'][key]['name'],
            Sync.from_config(config, key, datastore=datastore),
            Web.from_config(config, key, datastore=datastore)
        )
    
class Sync(Server):
    
    def __init__(self, name, synchronizers):
        super().__init__(self, name)
        self.synchronizers = list(synchronizers)
    
    def _start(self):
        for synchronizer in self.synchronizers:
            synchronizer.start()
        
    
    def _all_ok(self):
        return sum(s.isAlive() for s in self.synchronizers) == \
               len(self.synchronizers):
    
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
    def from_config(cls, config, key, datastore=None):
        
        if datastore == None:
            datastore = Datastore.from_config(
                    config, config['servers'][key]['datastore'])
                        
        synchronizers = []
        for k in config['servers'][key]['synchronizers']:
            synchronizer = Synchronizer.from_config(condig, k)
            synchronizer.set_datastore(datastore)
            synchronizers.append(synchronizer)
            
        
        return cls(
            config['servers'][key]['name'],
            synchronizers
        )

class Web(Server):
    
    def __init__(self, name, datastore, web_app):
        super().__init__(self, name)
        self.web_app = web_app
    
    def _start(self):
        self.web_app.start()
    
    def _all_ok(self):
        return self.web_app.isAlive()
    
    def _graceful_stop(self):
        self.web_app.stop()
    
    def status(self):
        doc = super().status()
        doc['web_app'] = self.web_app.status()
    
    @classmethod
    def from_config(cls, config, key, datastore=None):
        
        if datastore == None:
            datastore = Datastore.from_config(
                    config, config['servers'][key]['datastore'])
        
        
        web_app = WebApp.from_config(config, config['servers'][key]['web_app'])
        web_app.set_datastore(datastore)
        
        return cls(
            config['servers'][key]['name'],
            web_app
        )
    
