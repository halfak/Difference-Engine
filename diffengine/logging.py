from logging import logging

def load_config(config, name):
    
    logging.config.dictConfig(config[name])
