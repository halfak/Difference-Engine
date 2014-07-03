import sys;sys.path.insert(0, ".")
from pprint import pprint

from diffengine.difference import sequence_matcher, segment_matcher
from diffengine.segmenters import ParagraphsSentencesAndWhitespace

a = ["This", "is", "a", "sentence", ".", "  ", "This", "isn't", "a", "sentence", "."]
b = ["This", "isn't", "a", "sentence", ".", "  ", "This", "is", "a", "sentence", "."]

print("Longest common substring:")
for operation in sequence_matcher.diff(a,b):
    print("--> " + str(operation))

print("\n")
print("Segment matcher:")
for operation in segment_matcher.diff(a,b, segmenter=ParagraphsSentencesAndWhitespace()):
    print("--> " + str(operation))
