from .jsonobject import JsonObject


class Invite(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)
