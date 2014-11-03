import json
import logging

from gridfs import GridFS
from pymongo import MongoClient
from pymongo.errors import DocumentTooLarge

from .. import types
from .store import Store

logger = logging.getLogger("diffengine.stores.mongo")

class Mongo(Store):
    
    def __init__(self, db):
        self.db = db
        self.revisions = Revisions(self)
        self.engine_status = EngineStatus(self)
        self.processor_status = ProcessorStatus(self)
    
    @classmethod
    def from_params(cls, *args, db_name, **kwargs):
        client = MongoClient(*args, **kwargs)
        return cls(client[db_name])
    
    @classmethod
    def from_config(cls, config, name):
        return cls.from_params(
            host=config['stores'][name]['host'],
            port=config['stores'][name]['port'],
            db_name=config['stores'][name]['db_name'],
            w=config['stores'][name]['w']
        )
    
class Collection:
    
    ID_FIELD = NotImplemented
    
    def __init__(self, mongo):
        self.mongo = mongo
    
    def _mongoify(self, doc):
        doc['_id'] = doc[self.ID_FIELD]
        del doc[self.ID_FIELD]
        return doc
    
    def _demongoify(self, doc):
        doc[self.ID_FIELD] = doc['_id']
        del doc['_id']
        return doc
    
    
class Revisions(Collection):
    
    ID_FIELD = "rev_id"
    
    def store(self, revision):
        doc = self._mongoify(revision.to_json())
        
        logger.debug("Storing revision {0} with {1} operations.".format(
                    doc['_id'], len(doc['delta']['operations'])))
        
        try:
            self.mongo.db.revisions.save(doc)
        except DocumentTooLarge as e:
            delta = doc['delta']
            file_system = GridFS(self.mongo.db, "revisions")
            file_system.delete(doc['_id'])
            doc['delta'] = {'grid_id': doc['_id']}
            with file_system.new_file(_id=doc['_id'], encoding='utf-8') as f:
                
                json.dumps(delta, f)
            
            self.mongo.db.revisions.save(doc)
            
        
        logger.debug("Storing revision {0} stored!".format(doc['_id']))
        
        return True
    
    def query(self, rev_ids=None, page_id=None, after_id=None, before_id=None,
                    type=types.Revision):
        
        constraints = {}
        if rev_ids != None:
            constraints['rev_id'] = {'$in': rev_ids}
        if page_id != None:
            constraints['page_id'] = int(page_id)
        if after_id != None:
            constraints['rev_id'] = {'&gt': int(after_id)}
        if before_id != None:
            constraints['rev_id'] = {'&lt': int(before_id)}
        
        docs = self.mongo.db.revisions.find(constraints)
        
        for doc in docs:
            if 'grid_id' in doc['delta']:
                file_system = GridFS(self.mongo.db, "revisions")
                with file_system.get(doc['rev_id']) as f:
                    doc['delta'] = json.loads(f)
                
            yield Revision(self._demongoify(doc))
        

class EngineStatus(Collection):
    
    ID_FIELD = "engine_info"
    
    def store(self, status):
        assert isinstance(status, types.EngineStatus), str(status)
        doc = status.to_json()
        
        self.mongo.db.engine_status.save(self._mongoify(doc))
        self.mongo.db.engine_status.remove({'_id': {'$ne': doc['_id']}})
    
    def get(self, id=None, type=types.EngineStatus):
        docs = list(self.mongo.db.engine_status.find().limit(2))
        if len(docs) == 0:
            return None
        elif len(docs) > 1:
            logger.warning("More than one engine status found in " + \
                           "{0}.".format(self.mongo))
        
        return type(self._demongoify(docs[0]))
        


class ProcessorStatus(Collection):
    
    ID_FIELD = "page_id"
    
    def store(self, status):
        doc = status.to_json()

        self.mongo.db.processor_status.save(self._mongoify(doc))

    def get(self, page_id, type=types.ProcessorStatus):
        
        doc = self.mongo.db.processor_status.find_one(page_id)
        
        if doc is None: return None
        else:
            return type(self._demongoify(doc))
