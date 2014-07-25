from .. import util
from ..stores import Store
from ..wiki import Wiki


class Processor:
	
	def __init__(self, status):
		self.status = ProcessorStatus(status)
	
	def process(self, rev_id, timestamp, user, text):
		raise NotImplementedError()

class Engine:
	
	def __init__(self, wiki, store):
		self.wiki  = Wiki(wiki)
		self.store = Store(store)
	
	def info(self): raise NotImplementedError()
	
	def __str__(self): raise NotImplementedError()
	
	def __repr__(self): raise NotImplementedError()
	
	def get_processor(self, page_id):
		processor_status = self.store.processor_status.get(page_id)
		
		if processor_status is None:
			processor_status = self.PROCESSOR.STATUS(page_id)
		
		return self.PROCESSOR(processor_status, self.tokenizer, self.segmenter)
