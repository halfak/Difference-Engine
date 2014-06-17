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
    

class Revisions(Collection):
    
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
    
    def store(self, revision):
        doc = revision.to_json()
        
        self.mongo.db.revisions.save(self._mongoify(doc))
    
    def get(self, rev_ids, to_json=True):
        
        docs = self.mongo.db.revisions.find({'_id': {'$in': rev_ids}})
        
        for doc in docs:
            doc = self._demongoify(doc)
            
            if to_json:
                yield doc
            else:
                yield Delta.from_json(doc)
            
    
    
    def query(self, page_id=None, after_id=None, before_id=None, to_json=True):
        
        constraints = {}
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
        
