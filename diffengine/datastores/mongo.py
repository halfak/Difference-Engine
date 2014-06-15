from pymongo import MongoClient

from ..difference import Persist, Insert, Remove

class Mongo(Datastore):
    
    def __init__(self, db):
        self.db = db
        self.deltas = Deltas(self)
    
    
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
    

class Deltas(Collection):
    
    def __init__(self, mongo):
        self.mongo = mongo
    
    def _serialize_op(self, op, a, b):
        if isinstance(op, Persist):
            return {
                'op': "=",
                'a_start': op.start,
                'a_end': op.end,
                'b_start': offset,
                'b_end': offset + (op.end - op.start)
            }
        elif isinstance(op, Insert):
            return {
                'op': "+",
                'b_start': op.start,
                'b_end': op.end,
                'tokens': b[op.start, op.end]
            }
        elif isinstance(op, Remove):
            return {
                'op': "-",
                'a_start': op.start,
                'a_end': op.end,
                'tokens': a[op.start, op.end]
            }
        else:
            raise RuntimeError("Should never happen")
        
    
    
    def _serialize(self, delta):
        return {
            'rev_id': delta.rev_id,
            'page_id': delta.page_id,
            'ops': [_serialize_op(op) for op in ops]
        }
    
    def store(self, rev_id, page_id, a, b, ops):
        
        doc = {
            '_id': int(rev_id), # Indexed identifier
            'page_id': int(page_id),
            'ops': [_serialize_op(op, a, b) for op in ops
        }
        
        self.mongo.db.deltas.save(_serialize(delta), w="1")
    
    def _deserialize(self, doc):
        doc['rev_id'] = doc['_id']
        del doc['_id']
        return doc
    
    def get(self, rev_ids):
        
        docs = self.mongo.db.deltas.find({'_id': {'$in': rev_ids}})
        
        for doc in docs:
            yield self._deserialize(doc)
    
    def query(self, page_id=None, after_id=None, before_id=None):
        # TODO
        pass
        
