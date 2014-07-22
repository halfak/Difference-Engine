"""
Starts a daemon.

Usage:
    diff_daemon -h | --help
    diff_daemon <daemon> [--config=<path>]

Options:
    -h | --help      Shows this documentation
    <daemon>         The name of the server to start
    --config=<path>  The path to a configuration file
                     [default: ./config.yaml]
"""
from docopt import docopt

from diffengine import configuration, logging
from diffengine.daemons import Daemon

def main():
    args = docopt(__doc__) # Read args
    
    config = configuration.from_file(open(args['--config'])) # Get config
    
    run(config, args['<daemon>']) #

def run(config, daemon_name):
    
    # Logging from config
    logging_name = config['daemons'][daemon_name]['logging']
    logging.load_config(config['logging'][logging_name])
    
    # Construct from config
    daemon = Daemon.from_config(config, daemon_name)
    
    # Start
    daemon.start()
