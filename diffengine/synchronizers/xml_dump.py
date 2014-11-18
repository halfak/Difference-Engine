"""

Assumptions:

* Revisions appear ordered by page ASC, timestamp ASC, rev_id ASC
* The max(rev_id) and max(timestamp) of revisions represents the last revision
  chronologically captured by the dump
"""

import logging
import traceback

from mw.xml_dump import Iterator, map, open_file

from ..errors import RevisionOrderError
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
            try:
                for page in dump:
                    logger.debug("Constructing new processor for {0}:{1}"\
                                 .format(page.namespace, page.title))
                    
                    processor_status = self.store.processor_status.get(page.id,
                                              type=self.engine.Processor.Status)
                    
                    if processor_status is None:
                        processor_status = self.engine.Processor.Status(page.id)
                    
                    processor = self.engine.processor(processor_status)
                    
                    for rev in page:
                        if rev.id <= processor_status.last_rev_id:
                            
                            logger.debug(
                                    "Skipping revision (already processed) " +\
                                    "{0}:{1}".format(rev.id, rev.timestamp))
                            continue
                        try:
                            user = User(rev.contributor.id,
                                        rev.contributor.user_text)
                            delta = processor.process(rev.id, rev.timestamp,
                                                      rev.text)
                            revision = Revision(rev.id, rev.timestamp, page.id,
                                                user, delta)
                            yield (revision, None)
                        except RevisionOrderError as e:
                            logger.error(traceback.format_exc())
                            logger.info("Skipping revision (out of order) " + \
                                        "{0}:{1}".format(rev.id, rev.timestamp))
                    
                    logger.debug("Finished processing page {0}:{1}"\
                                 .format(page.namespace, page.title))
                    
                    yield (processor.status, page.title)
                
                logger.debug("Finished processing dump at {0}".format(path))
                yield (path, None)
            
            
            except Exception as e:
                logger.error(traceback.format_exc())
                raise
        
        engine_status = self.store.engine_status.get(type=self.engine.Status)
        if engine_status is None:
            logger.info("Starting {0} from scratch.".format(self.engine.info()))
            engine_status = self.engine.Status(self.engine.info())
        
        max_rev_id = 0
        max_timestamp = Timestamp(0)
        
        if len(self.paths) == 1:
            dump = Iterator.from_file(open_file(self.paths[0]))
            rev_proc_or_paths = _process_dump(dump, self.paths[0])
        else:
            rev_proc_or_paths = map(self.paths, _process_dump,
                                    **self.map_kwargs)
        
        try:
            for rev_proc_or_path, meta in rev_proc_or_paths:
                
                if isinstance(rev_proc_or_path, Revision):
                    revision = rev_proc_or_path
                    
                    self.store.revisions.store(revision)
                    self.status.stats['revisions_processed'] += 1
                    
                    max_rev_id = max(revision.rev_id, max_rev_id)
                    max_timestamp = max(revision.timestamp, max_timestamp)
                    
                elif isinstance(rev_proc_or_path, ProcessorStatus):
                    processor_status = rev_proc_or_path
                    page_title = meta
                        
                    logger.debug("Completed processing page " + \
                                 "{0}. {1}".format(
                                         page_title,
                                         processor_status.stats))
                    
                    self.store.processor_status.store(processor_status)
                    
                    
                elif isinstance(rev_proc_or_path, str):
                    path = rev_proc_or_path
                    
                    logger.info("Completed processing dump {0}".format(path))
                    
                else:
                    raise RuntimeError(
                            "Did not expect a " + \
                            "{0}".format(type(rev_proc_or_path)))
                
                
            
            self.status.update(max_rev_id, max_timestamp)
            
            self.store.engine_status.store(engine_status)
        
        except Exception as e:
            logger.error(traceback.format_exc())
            raise
