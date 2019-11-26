from .jsonobject import JSONObject
from .topic import Topic


# TODO: Parse out sub-categories into category objects if possible
class Category(JSONObject):
    def get_topics(self, page=None):
        params = {"page": page}
        return self.session.self.get("c/{}.json".format(self.id), params=params)

    # TODO: Override attribute calls to the below attributes to use update
    # function instead of returning the attribute
    def update(self, name, color=None, text_color=None):
        if not color:
            color = self.color
        if not text_color:
            color = self.text_color

        params = {"name": name, "color": color, "text_color": text_color}
        response = self.session.request(
            "PUT", "categories/{}.json".format(self.id), params=params
        )

        if response["success"] == "OK":
            self.update_attributes(**response["category"])
            return True
        return False


class CategoryList(JSONObject):
    pass
