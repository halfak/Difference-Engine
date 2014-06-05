from pprint import pprint

from diffengine.difference import hierarchical_matcher
from diffengine.tokenization import wikitext_split

tokens1 = wikitext_split.tokenize("Foo bar derp.")
print(tokens1)
for i, op in enumerate(hierarchical_matcher.diff([], tokens1)):
    print("#{0}: {1}".format(i+1, repr(op)))

print("-----------------------")

tokens2 = wikitext_split.tokenize("Foo bar derp. Foo bar derp.")
print(tokens2)
for i, op in enumerate(hierarchical_matcher.diff(tokens1, tokens2)):
    print("#{0}: {1}".format(i+1, repr(op)))


print("-----------------------")

tokens3 = wikitext_split.tokenize("Foo bar derp. Foo this is a bar derp.")
print(tokens3)
for i, op in enumerate(hierarchical_matcher.diff(tokens2, tokens3)):
    print("#{0}: {1}".format(i+1, repr(op)))
