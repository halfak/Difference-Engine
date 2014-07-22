from . import util

class Paths(util.SelfConstructor):
    
    def initialize(self, pages, scripts):
        self.pages = str(pages)
        self.scripts = str(scripts)
        
    
class Scripts(util.SelfConstructor):
    
    def initialize(self, index, api):
        self.index = str(index)
        self.api = str(api)
    


class Wiki(util.SelfConstructor):
    
    def initialize(self, name, protocol, domain, paths, scripts, port):
        self.name = str(name)
        self.protocol = str(protocol)
        self.domain = str(domain)
        self.paths = Paths(paths)
        self.scripts = Scripts(scripts)
        self.port = int(port)
