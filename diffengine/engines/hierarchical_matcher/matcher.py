
from . import defaults
from .. import ops, sequence_matcher
from ..difference_engine import DifferenceEngine
from ..ops import Insert, Persist, Remove
from .clustering import cluster, Paragraph, Sentence, Token, Whitespace


class HierarchicalMatcher(DifferenceEngine):
    def __init__(self,
                 tokenizer=defaults.TOKENIZER,
                 last=None,
                 min_group_size=defaults.MIN_GROUP_SIZE):
        self.tokenizer = tokenizer
        self.last = last or []
        self.min_group_size = int(min_group_size)
    
    def process(self, tokens):
        delta = diff(
            self.last,
            tokens,
            tokenizer=self.tokenizer,
            min_group_size=self.min_group_size
        )
        self.last = tokens
        
        return delta
        
    def serialize(self):
        return {
            'list': list(self.last)
        }
    
    @classmethod
    def deserialize(cls, doc, tokenizer=defaults.TOKENIZER):
        return cls(
            tokenizer=tokenizer,
            last=doc['last']
        )
    

def diff(a, b, tokenizer=defaults.TOKENIZER, min_group_size=defaults.MIN_GROUP_SIZE):
    
    a_clusters = cluster(a, tokenizer, min_size=min_group_size)
    b_clusters = cluster(b, tokenizer, min_size=min_group_size)
    
    
    # A cluster map from paragraphs and sentences
    a_cluster_map = {cluster:cluster
                     for cluster in a_clusters
                     if isinstance(cluster, Paragraph)}
    
    a_cluster_map.update({sequence:sequence
                          for paragraph in a_clusters
                          for sequence in paragraph
                          if isinstance(sequence, Sentence)})
    
    
    # Find matching content and flag it.
    b_processed_tokens = []
    for b_cluster in b_clusters:
        
        # Try to match paragraphs
        if b_cluster in a_cluster_map:
            a_cluster = a_cluster_map[b_cluster]
            a_cluster.add_match(b_cluster)
            b_cluster.add_match(a_cluster)
            b_processed_tokens.append(b_cluster)
            
        
        # Try to match sentences
        elif isinstance(b_cluster, Paragraph):
            
            for b_sequence in b_cluster:
                if b_sequence in a_cluster_map:
                    a_sequence = a_cluster_map[b_sequence]
                    a_sequence.add_match(b_sequence)
                    b_sequence.add_match(a_sequence)
                    b_processed_tokens.append(b_sequence)
                else:
                    b_processed_tokens.extend(b_sequence)
                
            
        else:
            #Add all unmatched tokens to the processed list
            b_processed_tokens.extend(db_cluster.tokens())
            
        
    
    
    # Produce new lists of unmatched tokens and matched clusters for A
    a_processed_tokens = []
    for a_cluster in a_clusters:
        
        if a_cluster.matched():
            a_processed_tokens.append(b_cluster)
        elif isinstance(a_cluster, Paragraph):
            for a_sequence in a_cluster:
                if a_sequence.matched():
                    a_processed_tokens.append(a_sequence)
                else:
                    a_processed_tokens.extend(a_sequence.tokens())
            
        else:
            a_processed_tokens.append(a_cluster.tokens())
    
    # Perform a final LCS and yield modified operations based on matched
    # clusters
    
    for op in sequence_matcher.diff(a_processed_tokens, b_processed_tokens):
        
        if isinstance(op, Persist):
            yield Persist(a_processed_tokens[op.start].start, a_processed_tokens[op.end-1].end)
            
        elif isinstance(op, Insert):
            
            inserted_tokens = []
            for tc in b_processed_tokens[op.start:op.end]:
                
                if isinstance(tc, Token):
                    inserted_tokens.append(tc)
                else:
                    if len(inserted_tokens) > 0:
                        yield Insert(inserted_tokens[0].start, inserted_tokens[-1].end)
                    
                    matched_cluster = tc.matches[0]
                    yield Persist(matched_cluster.start, matched_cluster.end)
                    
                    # reset!
                    inserted_tokens = []
                
            # Cleanup
            if len(inserted_tokens) > 0:
                yield Insert(inserted_tokens[0].start, inserted_tokens[-1].end)
            
        elif isinstance(op, Remove):
            removed_tokens = []
            for tc in a_processed_tokens[op.start, op.end]:
                
                if isinstance(tc, Token):
                    removed_tokens.append(tc)
                else: #Found a matched token... not removed -- just moved
                    if len(removed_tokens) > 0:
                        yield Remove(removed_tokens[0].start, removed_tokens[-1].end)
                    
                    # reset!
                    inserted_tokens = []
                
            # Cleanup
            if len(removed_tokens) > 0:
                yield Remove(removed_tokens[0].start, removed_tokens[-1].end)
                
        else:
            assert False, "Should never happen"
