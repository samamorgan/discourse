from .jsonobject import JsonObject
from .topic import Topic


class Category(JsonObject):

    Topic = Topic

    def __init__(self, client, json):
        self.client = client

        JsonObject.__init__(self, json)

    def update(self, name, color, text_color):
        return Category()

    def get_topics(self, id, page):
        return [Topic(), Topic()]
