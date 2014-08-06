import copy

from . import util


class Paths(util.SelfConstructor):
    __slots__ = ('pages', 'scripts')
    
    def initiate(self, pages, scripts):
        self.pages = str(pages)
        self.scripts = str(scripts)
        
    
class Scripts(util.SelfConstructor):
    __slots__ = ('index', 'api')
    
    def initiate(self, index, api):
        self.index = str(index)
        self.api = str(api)
    


class Wiki(util.SelfConstructor):
    __slots__ = ('name', 'dbname', 'protocol', 'domain', 'paths', 'scripts',
                 'port')
    def initiate(self, name, dbname, protocol, domain, paths, scripts, port):
        self.name = str(name)
        self.dbname = str(dbname)
        self.protocol = str(protocol)
        self.domain = str(domain)
        self.paths = Paths(paths)
        self.scripts = Scripts(scripts)
        self.port = int(port)
    
    def index_url(self):
        return self.protocol + "://" + self.domain + self.paths.scripts + \
               self.scripts.index
    
    def api_url(self):
        return self.protocol + "://" + self.domain + self.paths.scripts + \
               self.scripts.api
    
    @classmethod
    def from_config(cls, config, name):
        wiki_config = config['wikis'][name]
        
        kwargs = copy.deepcopy(wiki_config)
        kwargs['paths'] = Paths(**wiki_config['paths'])
        kwargs['scripts'] = Scripts(**wiki_config['scripts'])
        return cls(
            **kwargs
        )
