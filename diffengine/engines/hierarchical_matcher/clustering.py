from hashlib import sha1

from . import defaults

"""

This is a sentence.  This is the end.

This is another paragraph.

[
	Whitespace(0, 1, tokens=['\n']),
	Paragraph(1, 22, sequences=[
			Sentence(1, 9, blocks=['This', ' ', 'a', ' ', 'sentence', '.']),
			Whitespace(9, 10, tokens=['  ']),
			Sentence(10, 18, tokens=['This', ' ', 'is', ' ', 'the', ' ', 'end', '.'])
		]
	),
	Whitespace(18, 19, tokens=['\n\n']),
	Paragraph(19, 27, sequences=[
			Sentences(19, 27, tokens=['This', ' ', 'is', ' ', 'another', ' ', 'paragraph', '.'],
			Whitespace(27, 28, tokens=['\n'])
		]
	),
]
"""
def LookAhead(it):
	if isinstance(it, LookAheadType):
		return it
	else:
		return LookAheadType(it)

class LookAheadType:
	
	class DONE: pass
	
	def __init__(self, iterable):
		self.iterable = iter(iterable)
		
		self._load_next()
		
	def _load_next(self):
		try:
			self.next = next(self.iterable)
		except StopIteration:
			self.next = self.DONE
		
	def __next__(self):
		if self.empty():
			raise StopIteration()
		else:
			current = self.next
			self._load_next()
			return current
	
	def pop(self):
		return self.__next__()
	
	def peek(self):
		return self.next
	
	def empty(self):
		return self.next == self.DONE

class TokenCluster:
	
	def __init__(self, start, end, checksum):
		self.start = int(start)
		self.end = int(end)
		self.checksum = str(checksum)
		
	def __hash__(self):
		return hash(self.checksum)
	
	def __eq__(self, other):
		try:
			return self.checksum == other.checksum
		except AttributeError:
			raise TypeError("Cannot compare {0} to {1}.".format(type(self),
			                                                    type(other)))
	
	def __neq__(self, other):
		return not self == other
	
	def __len__(self):
		return self.end - self.start



class Token(TokenCluster):
	MATCHABLE = True
	
	def __init__(self, start, content):
		self.content = str(content)
		super().__init__(start, start+1, self.content)
	
	def __repr__(self):
		return repr(self.content)

class TokenSequence(TokenCluster, list):
	
	def __init__(self, start, end, tokens):
		hash = sha1()
		for token in tokens:
			hash.update(bytes(token.content, 'utf8'))
		
		TokenCluster.__init__(self, start, end, hash.digest())
		list.__init__(self, tokens)
	
	def __repr__(self):
		return "{0}({1}, {2}, {3})".format(
			self.__class__.__name__, 
			repr(self.start), 
			repr(self.end), 
			list.__repr__(self)
		)


class SequenceCollection(TokenCluster, list):
	
	def __init__(self, start, end, sequences):
		
		hash = sha1()
		for sequence in sequences:
			for token in sequence:
				hash.update(bytes(token.content, 'utf8'))
			
		
		TokenCluster.__init__(self, start, end, hash.digest())
		list.__init__(self, sequences)
	
	def __repr__(self):
		return "{0}({1}, {2}, {3})".format(
			self.__class__.__name__, 
			repr(self.start), 
			repr(self.end), 
			list.__repr__(self)
		)

class Paragraph(SequenceCollection): 
	MATCHABLE = True
	
class Sentence(TokenSequence): MATCHABLE = True
class Whitespace(TokenSequence): MATCHABLE = False

def read_whitespace(look_ahead, tokenizer, offset):
	#print("Reading whitespace.")
	
	whitespace_offset = offset
	whitespace_tokens = []
	
	while not look_ahead.empty() and tokenizer.WHITESPACE.match(look_ahead.peek()):
		whitespace_tokens.append(Token(offset, look_ahead.pop()))
		offset += 1
		
	
	assert len(whitespace_tokens) == offset - whitespace_offset
	return Whitespace(whitespace_offset, offset, whitespace_tokens)

def read_sentence(look_ahead, tokenizer, offset, min_size):
	#print("Reading sentence.")
	
	sentence_offset = offset
	sentence_tokens = []
	while not look_ahead.empty() and \
	      not tokenizer.PARAGRAPH_SPLIT.match(look_ahead.peek()):
		
		sentence_bit = look_ahead.pop()
		sentence_tokens.append(Token(offset, sentence_bit))
		offset += 1
		
		if tokenizer.SENTENCE_END.match(sentence_bit) and \
		   offset - sentence_offset >= min_size:
			break
		
	assert len(sentence_tokens) == offset - sentence_offset
	return Sentence(sentence_offset, offset, sentence_tokens)

def read_paragraph(look_ahead, tokenizer, offset, min_size):
	#print("Reading paragraph.")
	
	paragraph_offset = offset
	paragraph_sequences = []
	while not look_ahead.empty() and \
	      not tokenizer.PARAGRAPH_SPLIT.match(look_ahead.peek()):
		
		if tokenizer.WHITESPACE.match(look_ahead.peek()):
			sequence = read_whitespace(look_ahead, tokenizer, offset)
		else:
			sequence = read_sentence(look_ahead, tokenizer, offset, min_size)
			
		offset = sequence.end
		paragraph_sequences.append(sequence)
	
	return Paragraph(paragraph_offset, offset, paragraph_sequences)


def cluster(tokens, tokenizer, min_size=defaults.MIN_GROUP_SIZE):

	look_ahead = LookAhead(tokens)
	offset = 0
	
	clusters = []
	
	while not look_ahead.empty():
		if tokenizer.WHITESPACE.match(look_ahead.peek()):
			token_cluster = read_whitespace(look_ahead, tokenizer, offset)
		else:
			token_cluster = read_paragraph(look_ahead, tokenizer, offset, min_size)
		
		clusters.append(token_cluster)
		offset = token_cluster.end
	
	return clusters

