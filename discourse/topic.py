from .jsonobject import JsonObject
from .post import Post
from .user import User


class Topic(JsonObject):

    Post = Post

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def get_post(self, id):
        return self.get_posts([id])[0]

    def get_posts(self, post_ids):
        return [
            Post(client=self.client, json=post)
            for post
            in self.post_stream['posts']
            if post['id'] in post_ids
        ]

    def remove(self):
        response = self.client._request(
            'DELETE',
            't/{}.json'.format(self.id),
            params={'id': id}
        )

        return response.ok

    def update(self, title, category_id, slug='-'):
        response = self.client._request(
            'PUT',
            't/{}/{}.json'.format(slug, self.id),
            params={'title': title, 'category_id': category_id}
        )
        return Topic(client=self.client, json=response['basic_topic'])

    def invite_user(self, username):
        response = self.client._request(
            'POST',
            't/{}/invite'.format(self.id),
            params={'username': username}
        )
        return User(client=self.client, json=response['user'])

    def bookmark(self):
        response = self.client._request(
            'PUT',
            't/{}/bookmark'.format(self.id)
        )
        return response.ok

    def update_status(self, status, enabled, until):
        # TODO: Evaluate requirement of "until"
        response = self.client._request(
            'POST',
            't/{}/status'.format(self.id),
            params={
                'status': status,
                'enabled': enabled,
                'until': until,
            }
        )
        if response['success'] == 'OK':
            return True
        return False

    def timer(
        self,
        time,
        status_type,
        based_on_last_post,
        category_id
    ):
        response = self._request(
            'POST',
            't/{}/timer'.format(self.id),
            params={
                'time': time,
                'status_type': status_type,
                'based_on_last_post': based_on_last_post,
                'category_id': category_id,
            }
        )
        return response

    def update_timestamp(self, timestamp):
        response = self.client._request(
            'PUT',
            't/{}/change-timestamp'.format(self.id),
            params={'timestamp': timestamp}
        )
        if response['success'] == 'OK':
            return True
        return False

    def set_notification_level(self, notification_level):
        response = self.client._request(
            'POST',
            't/{}/notifications'.format(self.id),
            params={'notification_level': notification_level}
        )
        if response['success'] == 'OK':
            return True
        return False
