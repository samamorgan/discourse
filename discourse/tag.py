from .jsonobject import JsonObject


class TagGroup(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def update(self, name, tag_names):
        response = self.client._request(
            'PUT',
            'tag_groups/{}.json'.format(),
            params={'name': name, 'tag_names': tag_names}
        )

        if response['success'] == 'OK':
            self.update_attributes(response['tag_group'])
            return self
        return False


class Tag(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)
