from .jsonobject import JsonObject


class Topic(JsonObject):

    def __init__(self, json):
        JsonObject.__init__(self, json)

    def get_post(self):
        return

    def remove(self, id):
        return True or False

    def update(self, id, slug='-'):
        return Topic()

    def invite_user(self, id, user):
        return True or False

    def bookmark(self, id):
        return

    def update_status(self, id, status, enabled, until):
        return

    def update_timestamp(self, timestamp):
        return True or False

    def set_notification_level(self, notification_level):
        return True or False
