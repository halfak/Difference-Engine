from . import defaults
from .. import sequence_matcher
from ..ops import Insert, Persist, Remove
from .clustering import cluster, Paragraph, Sentence, Token


def diff(a, b, tokenizer=defaults.TOKENIZER,
               min_cluster_size=defaults.MIN_CLUSTER_SIZE):
    
    # Cluster the input token
    a_clusters = cluster(a, tokenizer, min_size=min_cluster_size)
    b_clusters = cluster(b, tokenizer, min_size=min_cluster_size)
    
    return diff_clusters(a_clusters, b_clusters)

def diff_clusters(a_clusters, b_clusters):
    
    # Matches and re-sequence unmatched tokens
    a_token_clusters, b_token_clusters = _match_clusters(a_clusters, b_clusters)
    
    # Perform a simple LCS over unmatched tokens and clusters
    clustered_ops = sequence_matcher.diff(a_token_clusters, b_token_clusters)
    
    # Return the expanded (de-clustered) operations
    return _expand_clustered_ops(clustered_ops,
                                 a_token_clusters,
                                 b_token_clusters)

def _build_cluster_map(a_clusters):
    # A cluster map from paragraphs and sentences
    cluster_map = {cluster:cluster
                   for cluster in a_clusters
                   if isinstance(cluster, Paragraph)}
    
    cluster_map.update({sequence:sequence
                        for paragraph in a_clusters
                        for sequence in paragraph
                        if isinstance(sequence, Sentence)})
    
    return cluster_map

def _match_clusters(a_clusters, b_clusters):
    
    a_cluster_map = _build_cluster_map(a_clusters)
    
    # Find matching content and flag it.
    b_token_clusters = []
    for b_cluster in b_clusters:
        
        # Try to match paragraphs
        if b_cluster in a_cluster_map:
            matched_cluster = a_cluster_map[cluster]
            matched_cluster.add_match(cluster)
            cluster.add_match(matched_cluster)
            b_token_clusters.append(cluster)
            
        
        # Try to match sentences
        elif isinstance(b_cluster, Paragraph):
            
            for sequence in b_cluster:
                if sequence in a_cluster_map:
                    matched_sequence = a_cluster_map[sequence]
                    matched_sequence.add_match(sequence)
                    sequence.add_match(matched_sequence)
                    b_token_clusters.append(sequence)
                else:
                    b_token_clusters.extend(sequence.tokens())
                
            
        else:
            #Add all unmatched tokens to the processed list
            b_token_clusters.extend(b_cluster.tokens())
        
    
    # Produce new lists of unmatched tokens and matched clusters for A
    a_token_clusters = []
    for a_cluster in a_clusters:
        
        # Check if a cluster is matched.
        if a_cluster.matched():
            a_token_clusters.append(a_cluster)
        
        elif isinstance(a_cluster, Paragraph): # cluster is a paragraph
            
            # Extracract the sentences and check for matches
            for a_sequence in a_cluster:
                if a_sequence.matched():
                    # It matched -- just append it
                    a_token_clusters.append(a_sequence)
                else:
                    # It didn't match, append it's tokens
                    a_token_clusters.extend(a_sequence.tokens())
            
        else:
            #Add all unmatched, non-paragraph tokens to the list
            a_token_clusters.extend(a_cluster.tokens())
        
    
    return a_token_clusters, b_token_clusters

def _expand_clustered_ops(ops, a_token_clusters, b_token_clusters):
    
    for op in ops:
        
        if isinstance(op, Persist):
            yield Persist(a_token_clusters[op.start].start, a_token_clusters[op.end-1].end)
            
        elif isinstance(op, Insert):
            
            inserted_tokens = []
            for token_or_cluster in b_token_clusters[op.start:op.end]:
                
                if isinstance(token_or_cluster, Token):
                    inserted_tokens.append(token_or_cluster)
                else:
                    if len(inserted_tokens) > 0:
                        yield Insert(inserted_tokens[0].start, inserted_tokens[-1].end)
                    
                    matched_cluster = token_or_cluster.matches[0]
                    yield Persist(matched_cluster.start, matched_cluster.end)
                    
                    # reset!
                    inserted_tokens = []
                
            # Cleanup
            if len(inserted_tokens) > 0:
                yield Insert(inserted_tokens[0].start, inserted_tokens[-1].end)
            
        elif isinstance(op, Remove):
            removed_tokens = []
            for token_or_cluster in a_token_clusters[op.start:op.end]:
                
                if isinstance(token_or_cluster, Token):
                    removed_tokens.append(token_or_cluster)
                else: #Found a matched token... not removed -- just moved
                    if len(removed_tokens) > 0:
                        yield Remove(removed_tokens[0].start, removed_tokens[-1].end)
                    
                    # reset!
                    removed_tokens = []
                
            # Cleanup
            if len(removed_tokens) > 0:
                yield Remove(removed_tokens[0].start, removed_tokens[-1].end)
                
        else:
            assert False, "Should never happen"
