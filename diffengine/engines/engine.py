from .. import util

class Engine:
	
	def __init__(self):
		raise NotImplementedError()
	
	def process(self):
		raise NotImplementedError()
	
	def str(self): self.repr()
	
	def repr(self): return util.instance.repr()
