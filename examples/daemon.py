"""
Starts a daemon.

Usage:
  diff_daemon <daemon> [--config=<path>]
  diff_daemon -h | --help

Options:
  -h --help        Shows this documentation
  <daemon>         The name of the server to start
  --config=<path>  The path to a configuration file
                   [default: ./config.yaml]
"""
import sys;sys.path.insert(0, ".")
from docopt import docopt
import logging

from diffengine import configuration, log

logger = logging.getLogger('daemon')

def main():
    args = docopt(__doc__)
    config = configuration.from_file(open(args['--config']))
    
    run(config, args['<daemon>'])

def run(config, daemon_name):
    
    logger_name = config['daemons'][daemon_name]['logger']
    log.load_config(config, logger_name)
    
    logger.info("Configuring daemon...")
    
    DaemonClass = \
            configuration.import_class(config['daemons'][daemon_name]['class'])
    
    daemon = DaemonClass.from_config(config, daemon_name)
    
    
    logger.info("Starting daemon: {0}".format(daemon))
    
    daemon.start()

if __name__ == "__main__": main()
