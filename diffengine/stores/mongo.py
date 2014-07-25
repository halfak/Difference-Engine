from pymongo import MongoClient

from .types import Revision

class Mongo(Datastore):
    
    def __init__(self, db):
        self.db = db
        self.revisions = Revisions(self)
    
    
    @classmethod
    def from_params(cls, *args, *, db_name, **kwargs):
        client = MongoClient(*args, **kwargs)
        return cls(client[db_name])
    
    @classmethod
    def from_config(cls, config, key):
        return cls.from_params(
            host=config[datastores][key]['host'],
            port=config[datastores][key]['port'],
            db_name=config[datastores][key]['db_name'],
            w=config[datastores][key]['w']
        )
    
class Collection:
    
    def __init__(self, mongo):
        self.mongo = mongo
    
    @classmethod
    def _mongoify(cls, doc):
        doc['_id'] = doc['rev_id']
        del doc['rev_id']
    
    @classmethod
    def _demongoify(cls, doc)
        doc['rev_id'] = doc['_id']
        del doc['_id']
    
    
class Revisions(Collection):
    
    def store(self, revision):
        doc = revision.to_json()
        
        self.mongo.db.revisions.save(self._mongoify(doc))
    
    def query(self, rev_ids=None, page_id=None, after_id=None, before_id=None,
                    to_json=True):
        
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
            doc = self._demongoify(doc)
            
            if to_json:
                yield doc
            else:
                yield Delta.from_json(doc)
        

class SychronizerStatus(Collection):
    
    def store(self, status):
        doc = status.to_json()
        
        self.mongo.db.synchronizer_status.store(self._mongoify(doc))
    
    def get(self, page_id): pass


class Processor(Collection):

    def store(self, status):
        doc = status.to_json()

        self.mongo.db.synchronizer_status.store(self._mongoify(doc))

    def get(self, page_id, ):
        
        
