"""
Converts XML dumps to edit diffs view WikiHadoop.  Due to limitations in
StreamWikiDumpInputFormat, this processor will exclude diffs for first edit of
a page.

Usage:
    ./wikihadoop_primer <engine> [--config=<path>]
    
Options:
    <engine>         The name of the engine that will be primed.  This is used
                     to configure an appropriate set of diff processors.
    --config=<path>  The path to a configuration file. [default: ./config.yaml]
"""
try:
    if os.path.exists("virtualenv"):
        sys.path.insert(0, "virtualenv")
        from bin import activate_this
    
    import json
    import logging
    import logging.config
    import profile
    import sys
    
    from docopt import docopt
    from mw import xml_dump

    from diffengine import configuration, errors
    from diffengine.engines import Engine
    from diffengine.types import Revision, User
    from diffengine.util import confirm

except:
    raise



def main():
    args = docopt(__doc__)
    config = configuration.from_file(open(args['--config']))
    
    run(config, args['<engine>'], sys.stdin)
    
def run(config, engine_name, page_xml_stream):
    
    engine = Engine.from_config(config, engine_name)
    dump = xml_dump.Iterator.from_page_xml(page_xml_stream)
    
    for page in dump:
        
        revisions = [revision for revision in page]
        
        if len(revisions) == 2:
            last, current = revisions
            delta = engine.diff(last.text, current.text)
            
            if current.contributor is not None:
                user_id = current.contributor.id
                user_text = current.contributor.user_text
            else:
                user_id = None
                user_text = None
            
            print(
                json.dumps(
                    Revision(
                        current.id,
                        current.timestamp,
                        current.sha1,
                        page.id,
                        User(user_id, user_text),
                        delta
                    ).to_json()
                )
            )
    

if __name__ == '__main__': main()
