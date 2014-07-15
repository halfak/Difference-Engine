import re

import deltas

class WikitextSplit(deltas.Tokenizer):
	
	def tokenize(self, text):
		return re.findall(
			r"[\w]+|[.?!]+|[\n\ \t\r]+|\[\[|\]\]|\{\{|\}\}|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
			text
		)
