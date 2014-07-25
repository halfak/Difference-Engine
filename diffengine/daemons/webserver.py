from .daemon import Daemon

class Webserver(Daemon):
    
    def __init__(self, name, webserver):
        super().__init__(self, name)
        self.webserver = webserver
    
    def _start(self):
        self.webserver.start()
    
    def _all_ok(self):
        return self.webserver.isAlive()
    
    def _graceful_stop(self):
        self.webserver.stop()
    
    def status(self):
        doc = super().status()
        doc['webserver'] = self.webserver.status()
    
    @classmethod
    def from_config(cls, config, key):
        
        webserver = WebApp.from_config(config, config['servers'][key]['web_app'])
        webserver.set_datastore(datastore)
        
        return cls(
            config['servers'][key]['name'],
            web_app
        )
