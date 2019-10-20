from .jsonobject import JsonObject


class TagGroup(JsonObject):
    def update(self, client, name, tag_names):
        response = client._request(
            "PUT",
            "tag_groups/{}.json".format(),
            params={"name": name, "tag_names": tag_names},
        )

        if response["success"] == "OK":
            self.update_attributes(response["tag_group"])
            return self
        return False


class Tag(JsonObject):
    pass
