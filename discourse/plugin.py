from .jsonobject import JsonObject


class Plugin(JsonObject):
    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)
