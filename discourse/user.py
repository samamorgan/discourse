from .jsonobject import JsonObject


class User(JsonObject):

    def __init__(self, client, **kwargs):
        self.client = client

        super().__init__(**kwargs)

    def update_avatar(self, upload_id, type):
        response = self._request(
            'PUT',
            'users/{}/preferences/avatar/pick'.format(self.username),
            params={'upload_id': upload_id, 'type': type}
        )

        # TODO: Update instance attribute for avatar on success
        if response['success'] == 'OK':
            return True
        return False

    def update_email(self, email):
        response = self._request(
            'PUT',
            'users/{}/preferences/email'.format(self.username),
            params={'email': email}
        )
        # TODO: Update instance attribute for avatar on success
        # TODO: Documentation unclear on response, investigate
        if response['success'] == 'OK':
            return True
        return False

    def delete(
        self,
        delete_posts=False,
        block_email=False,
        block_urls=False,
        block_ip=False,
    ):
        response = self._request(
            'DELETE',
            'admin/users/{}.json'.format(self.id),
            params={
                'delete_posts': delete_posts,
                'block_email': block_email,
                'block_urls': block_urls,
                'block_ip': block_ip,
            }
        )
        if response['deleted'] == 'true':
            return True
        return False

    def log_out(self):
        response = self._request(
            'POST',
            'admin/users/{}/log_out'.format(self.id),
        )
        if response['success'] == 'OK':
            return True
        return False

    def refresh_gravatar(self):
        return self._request(
            'POST',
            'user_avatar/{}/refresh_gravatar.json'.format(self.username),
        )

    def get_actions(self, offset, filter):
        # TODO: Create "Action" class
        return self._request(
            'GET',
            'user_actions.json',
            params={
                'offset': offset,
                'username': self.username,
                'filter': filter,
            }
        )
