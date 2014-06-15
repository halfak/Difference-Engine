from . import sequence_matcher
from ..segmenters import Token, MatchableSegment, MatchableSegmentNode, \
                         SegmentNodeCollection
from .ops import Insert, Persist, Remove


def diff(a, b, segmenter):
    
    # Cluster the input tokens
    a_segments = segmenter.segment(a)
    b_segments = segmenter.segment(b)
    
    return diff_segments(a_segments, b_segments)

def diff_segments(a_segments, b_segments):
    
    # Match and re-sequence unmatched tokens
    a_segment_tokens, b_segment_tokens = _cluster_matching_segments(a_segments,
                                                                    b_segments)
    
    # Perform a simple LCS over unmatched tokens and clusters
    clustered_ops = sequence_matcher.diff(a_segment_tokens, b_segment_tokens)
    
    # Return the expanded (de-clustered) operations
    return _expand_clustered_ops(clustered_ops,
                                 a_segment_tokens,
                                 b_segment_tokens)

def _build_segment_map(segments):
    segment_map = {}
    for segment in segments:
        if isinstance(segment, MatchableSegment):
            
            segment_map[segment] = segment
           
            if isinstance(segment, SegmentNodeCollection):
                # If the children are not tokens
                segment_map.update(_build_segment_map(segment))
    
    return segment_map


def _match_segments(a_segment_map, b_segments):
    for segment in b_segments:
        if isinstance(segment, MatchableSegment) and segment in a_segment_map:
            matched_segment = a_segment_map[segment]
            matched_segment.match = segment
            segment.match = matched_segment
            print("found match {0}".format(matched_segment))
            yield segment # Dump matched segment
            
        elif isinstance(segment, SegmentNodeCollection):
            yield from _match_segments(a_segment_map, segment) # Recurse
            
        else:
            yield from segment # Dump tokens
        
    
def _expand_unpatched_segments(a_segments):
    for segment in a_segments:
        # Check if a segment is matched.
        if isinstance(segment, MatchableSegment) and segment.match != None:
            yield segment # Yield matched segment as cluster
        elif isinstance(segment, SegmentNodeCollection):
            yield from _expand_unpatched_segments(segment) # Recurse
        else:
            yield from segment # Dump unmatched tokens

def _cluster_matching_segments(a_segments, b_segments):
    
    # Generate a look-up map for matchable segments in 'a'
    a_segment_map = _build_segment_map(a_segments)
    
    # Find and cluster matching content in 'b'
    b_segment_tokens = list(_match_segments(a_segment_map, b_segments))
    
    # Expand unmatched segments from 'a'
    a_segment_tokens = list(_expand_unpatched_segments(a_segments))
    
    return a_segment_tokens, b_segment_tokens

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
                    
                    matched_cluster = token_or_cluster.match
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
