from .jsonobject import JsonObject


class Invite(JsonObject):

    def __init__(self, json):
        JsonObject.__init__(self, json)
