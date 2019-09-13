from .json import JsonObject


class PrivateMessage(JsonObject):

    def __init__(self, json):
        JsonObject.__init__(self, json)
