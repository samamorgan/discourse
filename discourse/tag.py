from .json import JsonObject


class Tag(JsonObject):

    def __init__(self, json):
        JsonObject.__init__(self, json)
