from .jsonobject import JsonObject
from .post import Post


class Topic(JsonObject):

    Post = Post

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def get_post(self, id):
        return

    def remove(self):
        return True or False

    def update(self, slug='-'):
        return Topic()

    def invite_user(self, username):
        return True or False

    def bookmark(self):
        return

    def update_status(self, status, enabled, until):
        return

    def update_timestamp(self, timestamp):
        return True or False

    def set_notification_level(self, notification_level):
        return True or False
