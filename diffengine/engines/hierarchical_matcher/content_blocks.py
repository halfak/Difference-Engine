class ContentBlock:
	__slots__ = ('start', 'end', 'checksum')
	
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
			                                                    type(other))
	
	def __neq__(self, other):
		return not self == other
	
	def __len__(self):
		return self.end - self.start

class Paragraph(ContentBlock):
	__slots__ = ('sentences')
	
	def __init__(self, start, end, sentences):
		
		hash = sha1()
		for sentence in sentences:
			for token in sentence.tokens:
				hash.update(str(token.content, 'utf8'))
			
		
		super().__init__(start, end, hash.digest())
		self.sentences = list(sentences)
		
	
	
class Sentence(ContentBlock):
	__slots__ = ('tokens')
	
	def __init__(self, start, end, tokens):
		hash = sha1()
		for token in tokens:
			hash.update(str(token.content, 'utf8'))
		
		super().__init__(start, end, hash.digest())
		self.tokens = list(tokens)
	
class Whitespace(Sentence): pass

class Token(ContentBlock):
	def __init__(self, start, content):
		super.__init__(self, start, start+1, content)
	

def read_writespace(look_ahead, whitespace, offset):
	
	whitespace_offset = offset
	whitespace_tokens = []
	
	while not look_ahead.empty() and whitespace.match(look_ahead.peek()):
		whitespace_tokens.append(Token(offset, look_ahead.pop()))
		offset += 1
		
	
	return Whitespace(whitespace_offset, offset, whitespace_tokens)

def read_sentence(look_ahead, punctuation, offset, min_size):
	
	sentence_offset = offset
	sentence_tokens = []
	while not look_ahead.empty():
		sentence_bit = look_ahead.pop()
		whitespace_tokens.append(Token(offset, sentence_bit))
		offset += 1
		
		if punctuation.match(sentence_bit) and offset - sentence_offset >= min_size:
			break
		
	return Sentence(sentence_offset, offset, sentence_tokens)

def paragraphs(tokens,
               whitespace=defaults.WHITESPACE
               sentence_end=defaults.PUNCTUATION, 
               paragraph_split=defaults.DOUBLE_LINE,
               min_sentence_size=defaults.MIN_GROUP_SIZE):

	look_ahead = LookAhead(tokens)
	offset = 0
	
	while not look_ahead.empty():
		
		paragraphs = []
		
		if paragraph_split.match(look_ahead.peek()):
			
			whitespace = read_whitespace(look_ahead, whitespace, offset)
			offset = whitespace.end
			
			# Build and append the whitespace paragraph
			paragraphs.append(
				Paragraph(
					whitespace.start, whitespace.end, 
					[whitespace]
				)
			)
		else:
			paragraph_sentences = []
			paragraph_offset = offset
			
			#No more whitespace.  Time for us to get to work.  
			while not look_ahead.empty() and not paragraph_split.match(look_ahead.peek()):
				
				whitespace = read_whitespace(look_ahead, whitespace, offset)
				
				sentence = read_sentence(look_ahead, punctuation, offset, min_sentence_size)
				paragraph_sentences.append(sentence)
				
			
			paragraphs
				
				
		


def paragraphs(tokens,
               sentence_end=defaults.PUNCTUATION, 
               paragraph_split=defaults.DOUBLE_LINE,
               min_group_size=defaults.MIN_GROUP_SIZE):



	offset = 0
	paragraphs = []
	
	for matched, tokens in read_split(tokens, match=paragraph_split, min_match=min_group_size):
		
		if matched: # we found some inter-paragraph stuff
			
			whitespace_tokens = []
			for token in tokens:
				
				token = Token(offset, t_content)
				offset += 1
				whitespace_tokens.append(token)
			
			
			
		else:
			paragraph_offset = offset
			sentences = []
			
			for matched, tokens in read_split(pg_tokens, match=sentence_end, return_last=True, minsize=min_group_size):
				
				sentence_offset = offset
				sentence_tokens = []
				
				for t_content in sent_tokens:
					
					token = Token(offset, t_content)
					offset += 1
					sentence_tokens.append(token)
				
				sentences.append(Sentence(sentence_offset, offset, tokens))
			
			
			paragraphs.append(Paragraph(paragraph_offset, offset, sentences))
	
