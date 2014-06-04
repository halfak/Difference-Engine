from pprint import pprint

from diffengine.engines import SequenceMatcher
from diffengine.tokenization import wikitext_split

engine = SequenceMatcher()

for op in engine.process(wikitext_split.tokenize("Foo bar derp.")):
    pprint(op)
