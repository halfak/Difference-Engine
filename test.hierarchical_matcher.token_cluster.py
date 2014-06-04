from pprint import pprint

from diffengine.engines import hierarchical_matcher
from diffengine.tokenization import wikitext_split


input = "Foo bar derp."

tokens = wikitext_split.tokenize(input)
print(tokens)
for cluster in hierarchical_matcher.cluster(tokens, wikitext_split):
	pprint(cluster)

print("-----------------------")

input = """
This is a sentence.  This is the end.

This is another paragraph.
"""

tokens = wikitext_split.tokenize(input)
print(tokens)
for cluster in hierarchical_matcher.cluster(tokens, wikitext_split):
	pprint(cluster)

print("-----------------------")

input = """
This is a sentence.  This is the end.

This is another paragraph.
"""

tokens = wikitext_split.tokenize(input)
print(tokens)
for cluster in hierarchical_matcher.cluster(tokens, wikitext_split):
	pprint(cluster)

print("-----------------------")

input = """
== [[Wikipedia:WikiProject Articles for creation/Submissions|Article submissions]]==
* There are {{PAGESINCATEGORY:Pending AfC submissions}} pending submissions in [[:Category:Pending AfC submissions]].
* Declined submissions can be found in [[:Category:Declined AfC submissions]].
* Archives from before September 2008 can be found [[Wikipedia:Articles for creation/List|here]].
* Submissions are archived by date in [[:Category:AfC submissions by date]]:{{#categorytree:AfC submissions by date|depth=0}}

== [[Wikipedia:Articles for creation/Redirects|Redirects, categories]] and [[Wikipedia:Files for upload|files]] ==
* [[WP:Article wizard/Redirect|Redirect wizard]]
* [[WP:Article wizard/Category|Category wizard]]
* [[WP:Files for upload/Wizard|Files for upload wizard]]
"""

tokens = wikitext_split.tokenize(input)
print(tokens)
for cluster in hierarchical_matcher.cluster(tokens, wikitext_split):
	pprint(cluster)
