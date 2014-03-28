import re

DOUBLE_LINE = re.compile(r'[\n]{2,}')
PUNCTUATION = re.compile(r'[.?!]+')
WHITESPACE = re.compile(r'\n+| +|\t+')
MIN_GROUP_SIZE = 5
