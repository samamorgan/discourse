from .json import JsonObject


class Notification(JsonObject):

    def __init__(self, json):
        JsonObject.__init__(self, json)
