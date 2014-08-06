"""

Assumptions:

* Revisions appear ordered by page ASC, timestamp ASC, rev_id ASC
* The max(rev_id) and max(timestamp) of revisions represents the last revision
  chronologically captured by the dump
"""

import logging

from mw.xml_dump import Iterator, map, open_file

from .. import errors
from ..types import ProcessorStatus, Revision, Timestamp, User
from .synchronizer import Synchronizer

logger = logging.getLogger("diffengine.synchronizers.xml_dump")


class XMLDump(Synchronizer):
    
    def __init__(self, engine, store, paths, force_config=False, **map_kwargs):
        
        super().__init__(engine, store, force_config=force_config)
        self.paths = [str(path) for path in paths]
        self.map_kwargs = map_kwargs
    
    def run(self):
        
        def _process_dump(dump, path):
            for page in dump:
                logger.debug("Constructing new processor for {0}.".format(page.title))
                new_status = self.engine.Processor.Status(page.id)
                processor = self.engine.processor(new_status)
                
                for rev in page:
                    try:
                        user = User(rev.contributor.id, rev.contributor.user_text)
                        delta = processor.process(rev.id, rev.timestamp,
                                                  rev.text)
                        revision = Revision(rev.id, rev.timestamp, page.id,
                                            user, delta)
                        yield revision, None
                    except errors.RevisionOrderError as e:
                        logger.error(str(e))
                        logger.info("Skipping revision " + \
                                    "{0}:{1}".format(rev.id, rev.timestamp))
                        pass
                
                yield processor.status, page.title
            
            yield dump, path
        
        engine_status = self.store.engine_status.get(type=self.engine.Status)
        if engine_status is None:
            logger.info("Starting {0} from scratch.".format(self.engine.info()))
        
        max_rev_id = 0
        max_timestamp = Timestamp(0)
        
        if len(self.paths) == 1:
            dump = Iterator.from_file(open_file(self.paths[0]))
            revision_processor_or_dumps = _process_dump(dump, self.paths[0])
        else:
            revision_processor_or_dumps = map(self.paths, _process_dump,
                                             **self.map_kwargs)
        
        
        for revision_processor_or_dump, meta in revision_processor_or_dumps:
            
            if isinstance(revision_processor_or_dump, Revision):
                revision = revision_processor_or_dump
                
                self.store.revisions.store(revision)
                self.status.stats['revisions_processed'] += 1
                
                max_rev_id = max(revision.rev_id, max_rev_id)
                max_timestamp = max(revision.timestamp, max_timestamp)
                
            elif isinstance(revision_processor_or_dump, ProcessorStatus):
                processor_status = revision_processor_or_dump
                page_title = meta
                
                self.store.processor_status.store(processor_status)
                
                logger.debug("Completed processing page " + \
                             "{0}. {1}".format(page_title, processor_status.stats))
                
            elif isinstance(revision_processor_or_dump, xml_dump.Iterator):
                dump = revision_processor_or_dump
                path = meta
                
                logger.debug("Completed processing dump {0}".format(path))
                
            else:
                raise RuntimeError(
                        "Did not expect a " + \
                        "{0}".format(type(revision_processor_or_dump)))
        
        self.status.update(max_rev_id, max_timestamp)
        
        self.store.engine_status.store(self.status)
