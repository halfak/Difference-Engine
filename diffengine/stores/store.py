
import logging

from .. import configuration

logger = logging.getLogger("diffengine.stores.store")

class Store:
    
    @classmethod
    def from_config(cls, config, name):
        TokenizerClass = \
                configuration.import_class(config['stores'][name]['class'])
        return TokenizerClass.from_config(config, name)
