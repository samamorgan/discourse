from .jsonobject import JsonObject


class Group(JsonObject):
    def delete(self):
        response = self.client._request(
            "DELETE", "/admin/groups/{}.json".format(self.id)
        )

        if response["success"] == "OK":
            return True
        return False

    def get_members(self):
        return self.client._request("GET", "/groups/{}/members.json".format(self.name))

    def add_users(self, usernames):
        if type(usernames) is list:
            usernames = ",".join(usernames)

        response = self.client._request(
            "PUT",
            "/groups/{}/members.json".format(self.id),
            params={"usernames": usernames},
        )

        if response["success"] == "OK":
            return True
        return False

    def remove_users(self, usernames):
        # Need to understand the difference between:
        # - Remove user(s) from a group
        # - Remove group assigned to a user
        raise NotImplementedError

    def update(self):
        # TODO: Test what this actually does. This must take some sort of input.
        return self.client._request("PUT", "/groups/{name}.json")
