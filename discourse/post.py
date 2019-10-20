from .jsonobject import JsonObject


class Post(JsonObject):

    def update(self, client, raw=None, raw_old=None, edit_reason=None, cooked=None):
        response = client._request(
            'PUT',
            'posts/{}.json'.format(self.id),
            params={
                'post[raw]': raw,
                'post[raw_old]': raw_old,
                'post[edit_reason]': edit_reason,
                'post[cooked]': cooked,
            }
        )

        return Post(json=response['post'])

    def lock(self, client, locked):
        response = client._request(
            'PUT',
            'posts/{}/locked'.format(self.id),
            params={'locked': locked}
        )

        return response

    def action(self, client, action):
        # Must understand what the action fields represent before implementing
        # return Post(), True or False
        raise NotImplementedError
