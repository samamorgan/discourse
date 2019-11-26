from .jsonobject import JSONObject
from .post import Post
from .user import User


class Topic(JSONObject):
    def get_post(self, id):
        return self.get_posts([id])[0]

    def get_posts(self, post_ids):
        return [
            Post(self.session, **post)
            for post in self.post_stream["posts"]
            if post["id"] in post_ids
        ]

    def remove(self):
        params = {"id": id}
        response = self.session.request(
            "DELETE", "t/{}.json".format(self.id), params=params
        )

        return response.ok

    def update(self, title, category_id, slug="-"):
        params = {"title": title, "category_id": category_id}
        response = self.session.request(
            "PUT", "t/{}/{}.json".format(slug, self.id), params=params
        )

        self._update(**response["basic_topic"])

    def invite_user(self, username):
        params = {"username": username}
        return self.session.request(
            "POST", "t/{}/invite".format(self.id), params=params
        )

    def bookmark(self):
        return self.session.self.put("t/{}/bookmark".format(self.id))

    def update_status(self, status, enabled, until):
        # TODO: Evaluate requirement of "until"
        params = {"status": status, "enabled": enabled, "until": until}
        return self.session.request(
            "POST", "t/{}/status".format(self.id), params=params
        )

    def timer(self, time, status_type, based_on_last_post, category_id):
        params = {
            "time": time,
            "status_type": status_type,
            "based_on_last_post": based_on_last_post,
            "category_id": category_id,
        }
        return self.session.self.post("t/{}/timer".format(self.id), params=params)

    def update_timestamp(self, timestamp):
        params = {"timestamp": timestamp}
        return self.session.request(
            "PUT", "t/{}/change-timestamp".format(self.id), params=params
        )

    def set_notification_level(self, notification_level):
        params = {"notification_level": notification_level}
        return self.session.request(
            "POST", "t/{}/notifications".format(self.id), params=params
        )
