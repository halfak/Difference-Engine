from .jsonable_type import JsonableType

class User(JsonableType):
    __slots__ = ("user_id", "user_text")
    
    def initiate(self, user_id, user_text):
        self.user_id = int(user_id)
        self.user_text = str(user_text)
