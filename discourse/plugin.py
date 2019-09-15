from .jsonobject import JsonObject


class Plugin(JsonObject):

    def __init__(self, client, json):
        self.client = client

        JsonObject.__init__(self, json)
