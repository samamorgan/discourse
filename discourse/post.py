from .json import JsonObject


class Post(JsonObject):

    def __init__(self, json):
        JsonObject.__init__(self, json)

    def lock(self):
        return
