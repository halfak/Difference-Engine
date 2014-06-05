from nose.tools import eq_

from ..tokenization import wikitext_split
from .apply import apply


def test_diff_and_replay(diff):
    a = """
    This is a sentence. 712396912*(%^@#())?  ---231m1{}[][][[[]]]11 [] ]]]]
    
    ASDSJDNA  asas
    ...
    .
    This is another sentence.  Lorem ipsum?  LOREM IPSUM
    
    asd asd.as. ....as d.as.d .asd. as.d.as .asd.
    
                           hi
    
    
    """
    
    b = """
    This is a sentence. 23423423423*(%^333@#())?  ---231m1{}[11][][[[]]] [] ]]]]
    
    ASDSJDNA  asas
    This is   Lorem ipsum?  LOREM IPSUM
    
     whooooo
      
      asdas awdas das da sda ...a sdas .as. a.sd .as.d a.sd. as.d.
    
                another sentence           hi
    
    
    """
    a_tokens = wikitext_split.tokenize(a)
    b_tokens = wikitext_split.tokenize(b)
    delta = diff(a_tokens, b_tokens)
    
    replay_b_tokens = list(str(t) for t in apply(delta, a_tokens, b_tokens))
    
    eq_(b_tokens, replay_b_tokens)
