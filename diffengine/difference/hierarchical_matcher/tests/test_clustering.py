from nose.tools import eq_

from ... import util
from ....tokenization import wikitext_split
from ..clustering import cluster, Paragraph, Sentence, Token, Whitespace


def ts(contents):
    for i, content in enumerate(contents):
        yield Token(i, content)

def test_cluster():
    text =  "\n" + \
            "This is a sentence.  This is the end.\n" + \
            "\n" + \
            "This is another paragraph.\n"
    
    tokens = wikitext_split.tokenize(text)
    clusters = cluster(tokens, tokenizer=wikitext_split)
    tokens = list(ts(tokens)) # for comparison
    
    eq_(clusters,
        [
            Whitespace(0, 1, tokens=tokens[0:1]),
            Paragraph(1, 22, sequences=[
                    Sentence(1, 9, tokens=tokens[1:9]),
                    Whitespace(9, 10, tokens=tokens[9:10]),
                    Sentence(10, 18, tokens=tokens[10:18])
                ]
            ),
            Whitespace(18, 19, tokens=tokens[18:19]),
            Paragraph(19, 27, sequences=[
                    Sentence(19, 27, tokens=tokens[19:27]),
                    Whitespace(27, 28, tokens=tokens[27:28])
                ]
            ),
        ]
    )
