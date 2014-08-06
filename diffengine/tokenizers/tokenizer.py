import deltas.tokenizers

from .. import configuration


class Tokenizer(deltas.tokenizers.Tokenizer):

    @classmethod
    def from_config(cls, config, name):
        TokenizerClass = \
                configuration.import_class(config['tokenizers'][name]['class'])
        return TokenizerClass.from_config(config, name)
    
    def __str__(self): self.__repr__()
    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
