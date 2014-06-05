from pprint import pprint

from diffengine.difference import sequence_matcher
from diffengine.tokenization import wikitext_split

for op in sequence_matcher.diff([], wikitext_split.tokenize("Foo bar derp.")):
    pprint(op)
