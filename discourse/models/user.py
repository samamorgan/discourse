from .jsonobject import JSONObject
from .notification import Notification
from .private_message import PrivateMessage


class User(JSONObject):
    def update_avatar(self, upload_id, type):
        # TODO: Update instance attribute for avatar on success
        params = {"upload_id": upload_id, "type": type}
        return self.session.request(
            "PUT",
            "users/{}/preferences/avatar/pick".format(self.username),
            params=params,
        )

    def update_email(self, email):
        # TODO: Documentation unclear on response, investigate
        params = {"email": email}
        return self.session.request(
            "PUT", "users/{}/preferences/email".format(self.username), params=params
        )

    def delete(
        self, delete_posts=False, block_email=False, block_urls=False, block_ip=False
    ):
        params = {
            "delete_posts": delete_posts,
            "block_email": block_email,
            "block_urls": block_urls,
            "block_ip": block_ip,
        }
        return self.session.request(
            "DELETE", "admin/users/{}.json".format(self.id), params=params
        )

    def log_out(self):
        response = self.session.request(
            "POST", "admin/users/{}/log_out".format(self.id)
        )

        if response["success"] == "OK":
            return True
        return False

    def refresh_gravatar(self):
        return self.session.request(
            "POST", "user_avatar/{}/refresh_gravatar.json".format(self.username)
        )

    def get_actions(self, offset=None, filter=None):
        # TODO: Test and document useful values for parameters
        params = {"offset": offset, "username": self.username, "filter": filter}
        return self.session.self.get("user_actions.json", params=params)

    def get_private_messages(self):
        response = self.session.request(
            "GET", "topics/private-messages/{}.json".format(self.username)
        )

        return [
            PrivateMessage(self.session, **private_message)
            for private_message in response["topic_list"]["topics"]
        ]

    def get_private_messages_sent(self):
        response = self.session.request(
            "GET", "topics/private-messages-sent/{}.json".format(self.username)
        )

        return [
            PrivateMessage(self.session, **private_message)
            for private_message in response["topic_list"]["topics"]
        ]

    def get_notifications(self):
        params = {"username": self.username}
        response = self.session.self.get("notifications.json", params=params)

        return [
            Notification(**notification) for notification in response["notifications"]
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
