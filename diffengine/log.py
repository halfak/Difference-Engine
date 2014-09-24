import logging

DEFAULT = {
    'formatters': {
        'human': {
            'format': "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        }
    },
    'handlers': {
        'std_err': {
            'class': "logging.handlers.StreamHandler",
            'formatter': "human",
            'stream'  : "ext://sys.stdout",
            'level': "DEBUG"
        }
    },
    'loggers': {
        '': {
            'handlers': ["std_err"]
        }
    }
}

def load_config(config, name=None):
    logger_config_dict = config['loggers'].get(name, DEFAULT)
    logging.config.dictConfig(logger_config_dict)
