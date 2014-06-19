from collections import defaultdict

class SynchronizerStatus(JsonableType):
    
    def initialize(self, name, wiki, engine, tokenizer, state, stats):
        self.name = str(name)
        self.wiki = str(wiki)
        self.engine = str(engine)
        self.tokenizer = str(tokenize)
        self.state = dict(state)
        self.stats = defaultdict(stats, lambda: 0)
