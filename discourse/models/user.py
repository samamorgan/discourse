from .jsonobject import JsonObject
from .notification import Notification
from .private_message import PrivateMessage


class User(JsonObject):
    def update_avatar(self, upload_id, type):
        response = self.client._request(
            "PUT",
            "users/{}/preferences/avatar/pick".format(self.username),
            params={"upload_id": upload_id, "type": type},
        )

        # TODO: Update instance attribute for avatar on success
        if response["success"] == "OK":
            return True
        return False

    def update_email(self, email):
        response = self.client._request(
            "PUT",
            "users/{}/preferences/email".format(self.username),
            params={"email": email},
        )

        # TODO: Documentation unclear on response, investigate
        if response["success"] == "OK":
            return True
        return False

    def delete(
        self, delete_posts=False, block_email=False, block_urls=False, block_ip=False
    ):
        response = self.client._request(
            "DELETE",
            "admin/users/{}.json".format(self.id),
            params={
                "delete_posts": delete_posts,
                "block_email": block_email,
                "block_urls": block_urls,
                "block_ip": block_ip,
            },
        )

        if response["deleted"] == "true":
            return True
        return False

    def log_out(self):
        response = self.client._request(
            "POST", "admin/users/{}/log_out".format(self.id)
        )

        if response["success"] == "OK":
            return True
        return False

    def refresh_gravatar(self):
        return self.client._request(
            "POST", "user_avatar/{}/refresh_gravatar.json".format(self.username)
        )

    def get_actions(self, offset=None, filter=None):
        # TODO: Test and document useful values for parameters
        return self.client._request(
            "GET",
            "user_actions.json",
            params={"offset": offset, "username": self.username, "filter": filter},
        )

    def get_private_messages(self):
        response = self.client._request(
            "GET", "topics/private-messages/{}.json".format(self.username)
        )

        return [
            PrivateMessage(client=self.client, json=private_message)
            for private_message in response["topic_list"]["topics"]
        ]

    def get_private_messages_sent(self):
        response = self.client._request(
            "GET", "topics/private-messages-sent/{}.json".format(self.username)
        )

        return [
            PrivateMessage(client=self.client, json=private_message)
            for private_message in response["topic_list"]["topics"]
        ]

    def get_notifications(self):
        response = self.client._request(
            "GET", "notifications.json", params={"username": self.username}
        )

        return [
            Notification(json=notification)
            for notification in response["notifications"]
        ]

    def mark_notifications_read(self):
        # Not well documented in API. Need to reverse-engineer
        return NotImplementedError

    # Admin
    def suspend(self):
        # Combine suspend and unsuspend
        raise NotImplementedError

    def silence(self):
        # Combine silence and unsilence
        raise NotImplementedError

    def activate(self):
        raise NotImplementedError

    def anonymize(self):
        raise NotImplementedError

    def generate_api_key(self):
        raise NotImplementedError

    def assign_group(self):
        # Not clear exactly what this does from docs. Experiment.
        # Makes a user part of a group?
        raise NotImplementedError

    def remove_group(self):
        # Again, unclear what this does specificaly. May be able to combine
        # with assign_to_group
        raise NotImplementedError

    def send_password_reset_email(self):
        raise NotImplementedError

    def reset_password(self, password):
        raise NotImplementedError

    def get_badges(self):
        raise NotImplementedError

    def assign_badge(self, badge_id, reason):
        raise NotImplementedError

    def revoke_badge(self, id):
        raise NotImplementedError
