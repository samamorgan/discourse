from .jsonobject import JsonObject


class Plugin(JsonObject):

    def __init__(self, json):
        JsonObject.__init__(self, json)
