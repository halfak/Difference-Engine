"""
Primes a datastore with an XML dump.

Usage:
    xml_primer -h | --help
    xml_primer <datastore> <dump_path>... [--config=<path>]

Options:
    -h | --help      Shows this documentation
    <datastore>      The datastore to use
    --config=<path>  The path to a configuration file
                     [default: ./config.yaml]
"""
from docopt import docopt

from diffengine import configuration

def main():
    args = docopt(__doc__)
    config = configuration.from_file(open(args['--config']))
    
    run(config, args['<server_name>'])

def run(config, datastore):
    
    server_daemon = Server.from_config(config, SERVER_NAME)
    server_daemon.start()
