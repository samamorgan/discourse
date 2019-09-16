from .jsonobject import JsonObject


class User(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def update_avatar(self, upload_id, type):
        return True or False

    def update_email(self, email):
        return True or False

    def delete(self):
        return True or False

    def log_out(self):
        return True or False

    def refresh_gravatar(self):
        return True or False
