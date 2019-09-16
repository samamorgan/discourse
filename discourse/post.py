from .jsonobject import JsonObject


class Post(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def lock(self):
        return

    def update(self, id, raw, raw_old, edit_reason, cooked):
        return Post()

    def action(self, action):
        return Post(), True or False
