from pprint import pprint

from diffengine.engines import HierarchicalMatcher
from diffengine.tokenization import wikitext_split

engine = HierarchicalMatcher(tokenizer=wikitext_split)\


tokens = wikitext_split.tokenize("Foo bar derp.")
print(tokens)
for i, op in enumerate(engine.process(tokens)):
    print("#{0}: {1}".format(i+1, repr(op)))

print("-----------------------")

tokens = wikitext_split.tokenize("Foo bar derp. Foo bar derp.")
print(tokens)
for i, op in enumerate(engine.process(tokens)):
    print("#{0}: {1}".format(i+1, repr(op)))
