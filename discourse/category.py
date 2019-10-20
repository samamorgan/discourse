from .jsonobject import JsonObject
from .topic import Topic


# TODO: Parse out sub-categories into category objects if possible
class Category(JsonObject):
    def get_topics(self, client, page=None):
        response = client._request(
            "GET", "c/{}.json".format(self.id), params={"page": page}
        )

        return [Topic(json=topic) for topic in response["topic_list"]["topics"]]

    # TODO: Override attribute calls to the below attributes to use update
    # function instead of returning the attribute
    def update(self, client, name, color=None, text_color=None):
        if not color:
            color = self.color
        if not text_color:
            color = self.text_color

        response = client._request(
            "PUT",
            "categories/{}.json".format(self.id),
            params={"name": name, "color": color, "text_color": text_color},
        )

        if response["success"] == "OK":
            self.update_attributes(json=response["category"])
            return self
        return False
