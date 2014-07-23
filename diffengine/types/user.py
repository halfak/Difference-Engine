from .jsonable_type import JsonableType

class User(JsonableType):
    __slots__ = ("id", "text")
    
    def initiate(self, id, text):
        self.id = int(id)
        self.text = str(text)
