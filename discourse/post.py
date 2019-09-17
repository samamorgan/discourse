from .jsonobject import JsonObject


class Post(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def update(self, raw=None, raw_old=None, edit_reason=None, cooked=None):
        response = self.client._request(
            'PUT',
            'posts/{}.json'.format(self.id),
            params={
                'post[raw]': raw,
                'post[raw_old]': raw_old,
                'post[edit_reason]': edit_reason,
                'post[cooked]': cooked,
            }
        )

        return Post(client=self.client, json=response['post'])

    def lock(self, locked):
        response = self.client._request(
            'PUT',
            'posts/{}/locked'.format(self.id),
            params={'locked': locked}
        )

        return response

    def action(self, action):
        # Must understand what the action fields represent before implementing
        # return Post(), True or False
        raise NotImplementedError
