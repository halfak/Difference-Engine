import logging

from .. import configuration, util
from ..wiki import Wiki

logger = logging.getLogger("diffengine.engines.engine")

class Processor:
    
    def __init__(self, status):
        self.set_status(status)
    
    def set_status(self, status): raise NotImplementedError()
    
    def process(self, rev_id, timestamp, text):
        raise NotImplementedError()

class Engine:
    
    def __init__(self, name, wiki):
        self.name = str(name)
        self.wiki = Wiki(wiki)
    
    def info(self): raise NotImplementedError()
    
    def set_status(self, status, force_reconfig=False):
        if self.info() != status.engine_info:
            if force_reconfig:
                logger.warning("Overwriting engine status with " + \
                               "new configuration.\n" + \
                               " - stored: {0}\n".format(status.engine_info) + \
                               " - configured: {0}".format(self.info()))
                status.engine_info = self.info()
            else:
                raise ChangeWarning(
                        "Stored engine status does " + \
                        "not match configuration.\n" + \
                        " - stored: {0}\n".format(status.engine_info) + \
                        " - configured: {0}".format(self.info()))
            
        self.status = status
    

    def __str__(self): self.__repr__()
    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__,
                                 ", ".join(repr(v)
                                           for v in [self.name, self.wiki]))
    
    def processor(self, status): NotImplementedError()
    
    @classmethod
    def from_config(cls, config, name):
        EngineClass = \
                configuration.import_class(config['engines'][name]['class'])
        return EngineClass.from_config(config, name)
