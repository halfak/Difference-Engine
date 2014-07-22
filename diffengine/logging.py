from logging import logging

def load_config(config):
    
    logging.config.dictConfig(config[name])
