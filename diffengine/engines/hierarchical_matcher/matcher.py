
from .. import sequence_matcher, ops

from .content_blocks import blockify


class HierarchicalMatcher(DifferenceEngine):
	def __init__(self, 
	             last=None,
                 sentence_end=defaults.PUNCTUATION, 
                 paragraph_end=defaults.DOUBLE_LINE,
                 min_group_size=defaults.MIN_GROUP_SIZE):
		self.tokenizer = tokenizer
		self.last = last if last != None else []
		self.sentence_end = sentence_end
		self.paragraph_end = paragraph_end
		self.min_group_size = int(min_group_size)
	
	def process(self, tokens):
		delta = diff(
			last, 
			tokens,
			self.sentence_end,
			self.paragraph_end,
			self.min_group_size
		)
		self.last = tokens
		
		return delta
		
	def serialize(self):
		return {
			'list': list(self.last),
			'sentence_end': {
				'pattern': self.sentence_end.pattern,
				'flags': self.sentence_end.flags
			}
			'paragraph_end': {
				'pattern': self.paragraph_end.pattern,
				'flags': self.paragraph_end.flags
			}
			'min_group_size': self.min_group_size
		}
	
	@classmethod
	def deserialize(cls, doc, tokenizer=difference.simple_split):
		return cls(
			last=doc['last'], 
			sentence_end=re.compile(
				doc['sentence_end']['pattern'],
				flags=doc['sentence_end']['flags']
			)
			paragraph_end=re.compile(
				doc['paragraph_end']['pattern'],
				flags=doc['paragraph_end']['flags']
			),
			min_group_size=doc['min_group_size']
		)
	


def diff(a, b, 
         sentence_end=defaults.PUNCTUATION, 
         paragraph_end=defaults.DOUBLE_LINE,
         min_group_size=defaults.MIN_GROUP_SIZE):
	
	a_paragraphs = blockify(a, sentence_end=sentence_end, paragraph_end=paragraph_end, min_group_size=min_group_size)
	b_paragraphs = blockify(b, sentence_end=sentence_end, paragraph_end=paragraph_end, min_group_size=min_group_size)
	
	ops = []
	
	a_pg_map = {pg:pg for pg in a_paragraphs}
	
	matched_pgs = set()
	for b_paragraph in b_paragraphs:
		if b_paragraph in a_pg_map:
			a_paragraph = a_pg_map[b_paragraph]
			
			matched_pgs.add(a_paragraph)
			
			yield Persist(a_paragraph.start, a_paragraph.end, b_paragraph.start, b_paragraph.end)
		
	
	a_sentences = [s for s in pg for pg in a_paragraphs if pg not in matched_pgs]
	b_sentences = [s for s in pg for pg in b_paragraphs if pg not in matched_pgs]
	
	a_sentence_map = {s:s for s in a_sentences}
	
	matched_sentences = set()
	for b_sentence in (s for s in pg for pg in b_paragraphs):
		if b_sentence in a_sentence_map:
			a_sentence = a_sentence_map[a_sentence]
			
			matched_sentences.add(a_sentence)
			
			yield Persist(a_sentence.start, a_sentence.end, b_sentence.start, b_sentence.end)
	
	a_tokens = [t for t in s for s in a_sentences if s not in matched_sentences]
	b_tokens = [t for t in s for s in b_sentences if s not in matched_sentences]
	
	for op in sequence_matcher.diff(a_tokens, b_tokens):
		
		for op in sequential_token_ops(op, a_tokens, b_tokens):
			
	
