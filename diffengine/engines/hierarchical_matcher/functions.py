from . import defaults

def LookAhead(it):
	if isinstance(it, LookAhead):
		return it
	else:
		return LookAheadType(it)

class LookAheadType:
	
	class DONE: pass
	
	def __init__(self, iterable):
		if not hasattr(iterable, '__next__'):
			raise TypeError("iterable must be iterable")
		
	def _load_next(self):
		try:
			self.next = next(iterable)
		except StopIteration:
			self.next = self.DONE
		
	def __next__(self):
		if self.empty():
			raise StopIteration()
		else:
			return self.next
			self._load_next()
	
	def empty():
		self.next == self.DONE

def read_until(iterable, condition=lambda i, item: False, return_last=False):
	look_ahead = LookAhead(iterable)
	
	i = 0
	while not look_ahead.empty():
		if condition(i, look_ahead.peek()): 
			if return_last: yield look_ahead.pop()
			break
		
		yield look_ahead.pop()
		
		i += 1

def read_split(tokens, match, return_last, min_match=1):
	look_ahead = LookAhead(tokens)
	
	while not look_ahead.empty():
		yield False, read_until(
			look_ahead, 
			condition=lambda i, token: match.match(token) and (i+1) >= min_match,
			return_last=return_last
		)
		yield True, read_until(
			look_ahead, 
			condition=lambda i, token: not match.match(token)
		)

