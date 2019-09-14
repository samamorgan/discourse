from .jsonobject import JsonObject


class Category(JsonObject):

    def __init__(self, json):
        JsonObject.__init__(self, json)
