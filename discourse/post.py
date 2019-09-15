from .jsonobject import JsonObject


class Post(JsonObject):

    def __init__(self, client, json):
        self.client = client

        JsonObject.__init__(self, json)

    def lock(self):
        return

    def update(self, id, raw, raw_old, edit_reason, cooked):
        return Post()

    def action(self, action):
        return Post(), True or False
