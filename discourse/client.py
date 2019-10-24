import requests

from .category import Category
from .group import Group
from .plugin import Plugin
from .post import Post
from .private_message import PrivateMessage
from .tag import Tag, TagGroup
from .topic import Topic
from .user import User
from .web_hook import WebHook


class Client:

    Category = Category
    Group = Group
    Plugin = Plugin
    Post = Post
    PrivateMessage = PrivateMessage
    Tag = Tag
    TagGroup = TagGroup
    Topic = Topic
    User = User
    WebHook = WebHook

    def __init__(self, host, api_username="", api_key=""):
        # TODO: Better URL join method. If initialized without scheme, requests fail.
        self.host = host

        self.session = requests.Session()
        self.session.headers.update({"Api-Username": api_username, "Api-Key": api_key})

    # Class Methods
    def _request(self, method, path, params=None, data=None):
        response = self.session.request(
            method=method.upper(),
            url=requests.compat.urljoin(self.host, path),
            params=params,
            data=data,
        )
        response.raise_for_status()

        return response.json()

    # General
    def search(self, term, include_blurbs=True):
        # TODO: Parse json and pass back an array of objects
        response = self._request(
            "GET",
            "search/query.json",
            params={"term": term, "include_blurbs": include_blurbs},
        )

        return response

    def upload(self, files):
        response = self._request("POST", "uploads.json", params={"files": files})

        return response

    # Categories
    def get_category_list(self):
        response = self._request("GET", "categories.json")

        return [
            Category(client=self, json=category)
            for category in response["category_list"]["categories"]
        ]

    def create_category(self, name, color, text_color):
        response = self._request(
            "POST",
            "categories.json",
            params={"name": name, "color": color, "text_color": text_color},
        )

        return Category(client=self, json=response["category"])

    # Posts
    def get_latest_posts(self, before):
        # TODO: Figure out good default for before
        response = self._request("GET", "posts.json", params={"before": before})

        return [Post(client=self, json=post) for post in response["latest_posts"]]

    def get_group_posts(self, group_name):
        response = self._request("GET", "groups/{}/posts.json".format(group_name))

        return [Post(client=self, json=post) for post in response]

    def create_post(self, topic_id, raw):
        response = self._request(
            "POST", "posts.json", params={"topic_id": topic_id, "raw": raw}
        )

        return Post(client=self, json=response)

    def get_post_by_number(self, topic_id, post_number):
        response = self._request(
            "GET", "posts/by_number/{}/{}.json".format(topic_id, post_number)
        )

        return Post(client=self, json=response)

    def get_post(self, id):
        response = self._request("GET", "posts/{}.json".format(id))

        return Post(client=self, json=response)

    # Topics
    def create_topic(self, title, raw, category=None, created_at=None):
        response = self._request(
            "POST",
            "topics.json",
            params={
                "title": title,
                "raw": raw,
                "category": category,
                "created_at": created_at,
            },
        )

        return Topic(client=self, json=response)

    def get_topic(self, id, print=False):
        # print=True returns more details, and up to 1000 posts at once.
        # However, it is more heavily rate-limited by default.
        params = {"print": "true"} if print else {}
        response = self._request("GET", "t/{}.json".format(id), params=params)

        return Topic(client=self, json=response)

    def get_latest_topics(self, order, ascending=True):
        response = self._request(
            "GET", "latest.json", params={"order": order, "ascending": ascending}
        )

        return [
            Topic(client=self, json=topic) for topic in response["topic_list"]["topics"]
        ]

    def get_group_topics(self, group_name):
        response = self._request("GET", "topics/groups/{}.json".format(group_name))

        return [
            Topic(client=self, json=topic) for topic in response["topic_list"]["topics"]
        ]

    def get_top_topics(self, flag=""):
        if flag:
            flag = "/{}".format(flag)
        response = self._request("GET", "top{}.json".format(flag))

        return [
            Topic(client=self, json=topic) for topic in response["topic_list"]["topics"]
        ]

    # Invites
    def invite_user(self, email, group_names=None, custom_message=None):
        response = self._request(
            "POST",
            "invites",
            params={
                "email": email,
                "group_names": group_names,
                "custom_message": custom_message,
            },
        )

        if response["success"] == "OK":
            return User(client=self, json=response["user"])
        return False

    def generate_invite_url(self, email, group_names=None, custom_message=None):
        response = self._request(
            "POST",
            "invites/link",
            params={
                "email": email,
                "group_names": group_names,
                "custom_message": custom_message,
            },
        )

        return response

    # Private Messages
    def create_private_message(self, title, raw, target_usernames, created_at=None):
        response = self._request(
            "POST",
            "topics.json",
            params={
                "title": title,
                "raw": raw,
                "target_usernames": target_usernames,
                "archetype": "private_message",
                "created_at": created_at,
            },
        )

        return PrivateMessage(client=self, json=response)

    # Tags
    def get_tag_groups(self):
        response = self._request("GET", "tag_groups.json")

        return [
            TagGroup(client=self, json=tag_group)
            for tag_group in response["tag_groups"]
        ]

    def create_tag_group(self, name, tag_names):
        response = self._request(
            "POST", "tag_groups.json", params={"name": name, "tag_names": tag_names}
        )

        return TagGroup(client=self, json=response["tag_group"])

    def get_tag_group(self, id):
        response = self._request("GET", "tag_groups/{}.json".format(id))

        return TagGroup(client=self, json=response["tag_group"])

    def update_tag_group(self, id, name, tag_names):
        response = self._request(
            "PUT",
            "tag_groups/{}.json".format(),
            params={"name": name, "tag_names": tag_names},
        )

        return TagGroup(client=self, json=response["tag_group"])

    def get_tags(self):
        response = self._request("GET", "tags.json")
        return [Tag(client=self, json=tag) for tag in response["tags"]]

    def get_tag(self, tag):
        response = self._request("GET", "tags/{}.json".format(tag))
        response["id"] = tag

        return Tag(client=self, json=response)

    # Users
    def get_user(self, **kwargs):
        keyword_map = {
            "id": "admin/users/{}.json",
            "username": "users/{}.json",
            "external_id": "u/by-external/{}.json",
        }
        if len(kwargs) != 1:
            raise TypeError(
                "get_user() takes 1 keyword argument but {} were given".format(
                    len(kwargs)
                )
            )

        kw = list(kwargs)[0]
        if kw not in keyword_map:
            raise TypeError('"{}" is not a valid keyword argument.'.format(kw))

        response = self._request("GET", keyword_map[kw].format(kwargs[kw]))

        if kw == "id":
            return User(self, response)
        return User(client=self, json=response["user"])

    def create_user(
        self,
        name,
        email,
        password,
        username,
        active=True,
        approved=True,
        user_fields="",
    ):
        response = self._request(
            "POST",
            "users",
            params={
                "name": name,
                "email": email,
                "password": password,
                "username": username,
                "active": active,
                "approved": approved,
                "user_fields": user_fields,
            },
        )

        return self.get_user(id=response["user_id"])

    def get_public_users(self, period, order, ascending=True, page=0):
        response = self._request(
            "GET",
            "directory_items.json",
            params={
                "period": period,
                "order": order,
                "ascending": ascending,
                "page": page,
            },
        )

        # TODO: Return more than just the users here
        return [
            User(client=self, json=user) for user in response["directory_items"]["user"]
        ]

    def get_users(self, flag, order, ascending=True, page=None, show_emails=None):
        response = self._request(
            "GET",
            "admin/users/list/{}.json".format(self.flag),
            params={
                "order": order,
                "ascending": ascending,
                "page": page,
                "show_emails": show_emails,
            },
        )

        return [User(client=self, json=user) for user in response]

    # Upload

    # Search

    # Admin Emails
    def show_email_settings(self):
        return self._request("GET", "admin/email.json")

    def show_email_templates(self):
        return self._request("GET", "admin/customize/email_templates.json")

    # Admin

    # Groups
    def get_group(self, name):
        response = self._request("GET", "groups/{}.json".format(name))

        return Group(client=self, json=response["group"])

    # Password Reset

    # Site Settings
    def show_site_settings(self):
        # May be able to make an overall "Site Settings" def
        return self._request("GET", "admin/site_settings.json")

    # Plugins
    def get_plugins(self):
        response = self._request("GET", "admin/plugins")

        return [Plugin(client=self, json=plugin) for plugin in response]

    # Backups
    def get_backups(self):
        return self._request("GET", "/admin/backups.json")

    def create_backup(self, with_uploads):
        response = self._request(
            "POST", "/admin/backups.json", params={"with_uploads": with_uploads}
        )

        if response["success"] == "OK":
            return True
        return False

    def download_backup(self, filename):
        # TODO: Undocumented response, reverse-engineer it
        return self._request("PUT", "/admin/backups/{}".format(filename))

    def set_backup_readonly(self, enable):
        # TODO: Documented as empty response. Check it out and return
        #       something useful.
        return self._request(
            "PUT", "/admin/backups/readonly", params={"enable": enable}
        )

    # Emails
    def get_emails(self, action, offset):
        # TODO: Offset doesn't appear to be a part of the request syntax.
        #       Need to test and figure out correct request and returns.
        actions = ["sent", "skipped", "bounced", "received", "rejected"]
        if action not in actions:
            raise ValueError('"action" must be one of: {}'.format(actions))

        response = self._request(
            "GET", "/admin/emails/{}.json".format(action), params={"offset": offset}
        )

        return response

    # Flags
    def get_flags(self, type, offset):
        types = ["active", "old"]
        if type not in types:
            raise ValueError('"type" must be one of: {}'.format(types))

        response = self._request(
            "GET", "/admin/flags/{}.json".format(type), params={"offset": offset}
        )

        return response

    # Badges
    def get_badges(self):
        # TODO: Make a Badge class. Return Badge() list
        return self._request("GET", "/admin/badges.json")

    def create_badge(
        self,
        allow_title,
        multiple_grant,
        listable,
        auto_revoke,
        enabled,
        show_posts,
        target_posts,
        name,
        description,
        long_description,
        icon,
        image,
        badge_grouping_id,
        badge_type_id,
    ):
        response = self._request(
            "POST",
            "/admin/badges.json",
            params={
                "allow_title": allow_title,
                "multiple_grant": multiple_grant,
                "listable": listable,
                "auto_revoke": auto_revoke,
                "enabled": enabled,
                "show_posts": show_posts,
                "target_posts": target_posts,
                "name": name,
                "description": description,
                "long_description": long_description,
                "icon": icon,
                "image": image,
                "badge_grouping_id": badge_grouping_id,
                "badge_type_id": badge_type_id,
            },
        )

        if response["success"] == "OK":
            return True
        return False

    # User Fields
    def get_user_fields(self):
        return self._request("GET", "/admin/customize/user_fields.json")

    def create_user_field(self, name, description, field_type, required):
        return self._request(
            "POST",
            "/admin/customize/user_fields.json",
            params={
                "user_field[name]": name,
                "user_field[description]": description,
                "user_field[field_type]": field_type,
                "user_field[required]": required,
            },
        )

    def delete_user_field(self, id):
        response = self._request(
            "DELETE", "/admin/customize/user_fields/{id}", params={"id": id}
        )

        if response["success"] == "OK":
            return True
        return False

    # Web Hooks
    def create_web_hook(
        self,
        payload_url,
        content_type,
        secret,
        wildcard_web_hook,
        verify_certificate,
        active,
        web_hook_event_type_ids,
        category_ids,
        group_ids,
    ):
        response = self._request(
            "POST",
            "/admin/api/web_hooks",
            params={
                "payload_url": payload_url,
                "content_type": content_type,
                "secret": secret,
                "wildcard_web_hook": wildcard_web_hook,
                "verify_certificate": verify_certificate,
                "active": active,
                "web_hook_event_type_ids": web_hook_event_type_ids,
                "category_ids": category_ids,
                "group_ids": group_ids,
            },
        )

        return WebHook(client=self, json=response)

    # Logs
    def get_staff_action_logs(self, action_name, action_id):
        return self._request(
            "GET",
            "/admin/logs/staff_action_logs.json",
            params={"action_name": action_name, "action_id": action_id},
        )

    # About
    def fetch_about(self):
        return self._request("GET", "/about.json")

    # Poll Plugin
    def poll_vote(self, post_id, poll_name, options):
        # May be best to implement in Post class. Investigate
        response = self._request(
            "PUT",
            "/polls/vote",
            params={"post_id": post_id, "poll_name": poll_name, "options": options},
        )

    # Reports
    def get_pageview_stats(self, start_date, end_date, category_id, group_id):
        return self._request(
            "GET",
            "/page_view_total_reqs",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "category_id": category_id,
                "group_id": group_id,
            },
        )

    def get_site_configuration(self):
        response = self._request("GET", "site.json")

        return response

    def export_report(self, entity, name, start_date, end_date, group_id):
        response = self._request(
            "POST",
            "/export_csv/export_entity.json",
            params={
                "entity": entity,
                "args[name]": name,
                "args[start_date]": start_date,
                "args[end_date]": end_date,
                "args[group_id]": group_id,
            },
        )

        if response["success"] == "OK":
            return True
        return False
