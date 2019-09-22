from .jsonobject import JsonObject


class Group(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def delete(self):
        raise NotImplementedError

    def get_members(self):
        raise NotImplementedError

    def add_users(self, usernames):
        if type(usernames) is str:
            if ',' in usernames:
                usernames = usernames.split(',')
        raise NotImplementedError

    def remove_users(self, usernames):
        # Need to understand the difference between:
        # - Remove user(s) from a group
        # - Remove group assigned to a user
        if type(usernames) is str:
            if ',' in usernames:
                usernames = usernames.split(',')
        raise NotImplementedError

    def update(self):
        return NotImplementedError
