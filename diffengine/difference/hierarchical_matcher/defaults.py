import re

from ...tokenizers import WikitextSplit

DOUBLE_LINE = re.compile(r'[\n]{2,}')
PUNCTUATION = re.compile(r'[.?!]+')
WHITESPACE = re.compile(r'\n+| +|\t+')
MIN_CLUSTER_SIZE = 5
TOKENIZER = WikitextSplit()
