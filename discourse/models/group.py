from .jsonobject import JSONObject


class Group(JSONObject):
    def delete(self):
        return self.session.self.delete("/admin/groups/{}.json".format(self.id))

    def get_members(self):
        return self.session.self.get("/groups/{}/members.json".format(self.name))

    def add_users(self, usernames):
        if type(usernames) is list:
            usernames = ",".join(usernames)

        params = {"usernames": usernames}
        return self.session.request(
            "PUT", "/groups/{}/members.json".format(self.id), params=params
        )

    def remove_users(self, usernames):
        # Need to understand the difference between:
        # - Remove user(s) from a group
        # - Remove group assigned to a user
        raise NotImplementedError

    def update(self):
        # TODO: Test what this actually does. This must take some sort of input.
        return self.session.self.put("/groups/{name}.json")
