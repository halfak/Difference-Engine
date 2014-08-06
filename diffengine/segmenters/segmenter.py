import logging

import deltas.segmenters

from .. import configuration

logger = logging.getLogger("diffengine.segmenters.segmenter")


class Segmenter(deltas.segmenters.Segmenter):
    
    
    @classmethod
    def from_config(cls, config, name):
        SegmenterClass = \
                configuration.import_class(config['segmenters'][name]['class'])
        return SegmenterClass.from_config(config, name)
