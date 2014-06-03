import re

def tokenize(text):
	return re.findall(
		r"[\w]+|[.?!]+|\[\[|\]\]|\{\{|\}\}|\n+| +|\t+|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
		text
	)

WHITESPACE = re.compile(r"[\n\t\ ]+")
PARAGRAPH_SPLIT = re.compile(r"[\n]{2,}")
SENTENCE_END = re.compile(r"[.?!]+")
