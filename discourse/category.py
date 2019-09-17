from .jsonobject import JsonObject
from .topic import Topic


class Category(JsonObject):

    Topic = Topic

    def __init__(self, client, **kwargs):
        # TODO: Parse out sub-categories into category objects if possible
        self.client = client

        super().__init__(**kwargs)

    def get_topics(self, page=None):
        response = self.client._request(
            'GET',
            'c/{}.json'.format(self.id),
            params={'page': page}
        )

        return [
            Topic(client=self.client, json=topic)
            for topic
            in response['topic_list']['topics']
        ]

    # TODO: Override attribute calls to the below attributes to use update
    # function instead of returning the attribute
    def update(self, name, color=None, text_color=None):
        if not color:
            color = self.color
        if not text_color:
            color = self.text_color

        response = self.client._request(
            'PUT',
            'categories/{}.json'.format(self.id),
            params={'name': name, 'color': color, 'text_color': text_color}
        )

        # TODO: Figure out actual string values of response['success']
        if response['success'] == 'Foo':
            return Category(client=self.client, json=response['category'])
        return False
