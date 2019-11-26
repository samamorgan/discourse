from .jsonobject import JSONObject


class Tag(JSONObject):
    pass


class TagGroup(JSONObject):
    def update(self, session, name, tag_names):
        params = {"name": name, "tag_names": tag_names}
        response = session.self.put("tag_groups/{}.json".format(), params=params)

        if response["success"] == "OK":
            self.update_attributes(response["tag_group"])
            return True
        return False
