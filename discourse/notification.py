from .jsonobject import JsonObject


class Notification(JsonObject):

    def __init__(self, client, json):
        self.client = client

        JsonObject.__init__(self, json)
