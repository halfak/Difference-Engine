


class DifferenceEngine:
	
	def __init__(self):
		raise NotImplementedError()
	
	def process(self):
		raise NotImplementedError()
	
	def serialize(self):
		raise NotImplementedError()
		
	@classmethod
	def deserialize(self, doc):
		raise NotImplementedError()
