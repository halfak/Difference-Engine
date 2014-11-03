"""
Primes a datastore with an XML dump.

Usage:
    primer -h | --help
    primer <engine> <store> <dump_path>... [--config=<path>]
                                           [--logger=<logging>]
                                           [--profile]
                                           [--threads=<count>]

Options:
    -h --help          Shows this documentation
    <engine>           The name of engine to prime
    <store>            The name of store to prime
    --config=<path>    The path to a configuration file
                       [default: ./config.yaml]
    --logger=<logger>  Which logging configuration to use
                       [default: debug]
    --profile          Produce profiling information
    --threads=<count>  How many threads to start up?
"""
import logging
import logging.config
import profile
import sys

from docopt import docopt

from diffengine import configuration, errors, log
from diffengine.engines import Engine
from diffengine.stores import Store
from diffengine.synchronizers import XMLDump
from diffengine.util import confirm

logger = logging.getLogger("primer")

def main():
    args = docopt(__doc__)
    config = configuration.from_file(open(args['--config']))
    
    start = lambda: run(config, args['<engine>'], args['<store>'],
                                args['<dump_path>'], args['--logger'],
                                args['--threads'])
    
    try:
        if args['--profile']:
            stats = profile.runctx("start()", globals(), locals())
        else:
            start()
    finally:
        if args['--profile']:
            print(stats)
    

def run(config, engine_name, store_name, paths, logger_name, threads):
    
    threads = int(threads) if threads is not None else None
    
    log.load_config(config, logger_name)
    
    logger.info("Configuring primer...")
    
    
    engine = Engine.from_config(config, engine_name)
    store = Store.from_config(config, store_name)
    
    try:
        primer = XMLDump(engine, store, paths, threads=threads)
    except errors.ChangeWarning as e:
        print(str(e))
        if confirm("Would you like to continue anyway?", default="no",
                   stream=sys.stderr):
            primer = XMLDump(engine, store, paths,
                             force_config=True, threads=threads)
        else:
            sys.exit(1)
    
    logger.info("Starting primer:\n" +
                " - engine: {0}\n".format(engine) +
                " - paths: {0}".format(len(paths)))
    
    primer.start()

if __name__ == "__main__": main()
