from collections import defaultdict

class SynchronizerStatus(JsonableType):
    
    def initialize(self, name, wiki, engine, tokenizer, last_rev_id,
                         last_timestamp, stats):
        self.name = str(name)
        self.wiki = str(wiki)
        self.engine = str(engine)
        self.last_rev_id = int(last_rev_id)
        self.last_timestamp = int(last_timestamp)
        self.stats = defaultdict(stats, lambda: 0)
