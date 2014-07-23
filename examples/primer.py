"""
Primes a datastore with an XML dump.

Usage:
    xml_primer -h | --help
    xml_primer <datastore> <dump_path>... [--config=<path>] [--logging=<logging>]

Options:
    -h | --help        Shows this documentation
    <engine>           The name of engine to prime
    --config=<path>    The path to a configuration file
                       [default: ./config.yaml]
    --logger=<logger>  Which logging configuration to use
"""
from docopt import docopt
import logging

from diffengine import configuration, log
from diffengine.synchronizers import XMLDumpPrimer

logger = logging.getLogger("primer")

def main():
    args = docopt(__doc__)
    config = configuration.from_file(open(args['--config']))
    
    run(config, args['<engine>'], args['<dump_path>'], args['--logger'])

def run(config, engine_name, paths, logger_name):
    
    log.load_config(config, logger_name)
    
    logger.info("Configuring primer...")
    
    EngineClass = \
            configuration.import_class(config['engine'][engine_name]['class'])
    
    engine = EngineClass.from_config(config, engine_name)
    
    primer = XMLDumpPrimer(engine, paths)
    
    logger.info("Starting primer:\n" +
                " - engine: {0}\n".format(engine) +
                " - paths: {0}".format(len(paths)))
    
    primer.start()
