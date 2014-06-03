
from .. import sequence_matcher, ops

from .clustering import cluster, Paragraph, Sentence, Whitespace


class HierarchicalMatcher(DifferenceEngine):
	def __init__(self, 
                 tokenizer,
	             last=None):
		self.tokenizer = tokenizer
	
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
			'list': list(self.last)
		}
	
	@classmethod
	def deserialize(cls, doc, tokenizer=tokenization.wikitext_split):
		return cls(
			tokenizer=tokenizer,
			last=doc['last']
		)
	


def delta_ops(a, b, min_group_size=defaults.MIN_GROUP_SIZE):
	
	a_clusters = cluster(a, tokenizer, min_size=min_group_size)
	b_clusters = cluster(b, tokenizer, min_size=min_group_size)
	
	inserts = []
	copies = []
	removals = []
	
	a_cluser_map = {}
	for cluster in a_clusters:
		if isinstance(cluster, Paragraph):
			a_cluser_map[cluster] = cluster
			
			for sequence in cluster:
				
				if isinstance(cluster, Sentence):
					a_cluser_map[cluster] = 
	
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
			
	
