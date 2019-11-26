import json

import requests

from .models import *


class Session(requests.Session):
    def __init__(self, host, api_username="", api_key=""):
        # TODO: Better URL join method. If initialized without scheme, requests fail.
        super().__init__()
        self.host = host
        self.headers.update({"Api-Username": api_username, "Api-Key": api_key})

    # Class Methods
    def request(self, method, path, **kwargs):
        response = super().request(
            method, requests.compat.urljoin(self.host, path), **kwargs
        )
        response.raise_for_status()

        return response.json(object_hook=self._object_hook)

    category = Category
    category_list = CategoryList
    group = Group
    grouped_search_result = GroupedSearchResult
    notification = Notification
    plugin = Plugin
    post = Post
    private_message = PrivateMessage
    site = Site
    tag = Tag
    tag_group = TagGroup
    topic = Topic
    user = User
    web_hook = WebHook

    def _object_hook(self, dct):
        # TODO: There's definitely a more elegant way to do this.
        if "categories" in dct:
            dct["categories"] = [Category(self, **cat) for cat in dct["categories"]]
        if "groups" in dct:
            dct["groups"] = [Group(self, **group) for group in dct["groups"]]
        for i in ["posts", "latest_posts"]:
            if i in dct:
                dct[i] = [Post(self, **post) for post in dct[i]]
        if "tags" in dct:
            dct["tags"] = [Tag(self, **tag) for tag in dct["tags"]]
        if "topics" in dct:
            dct["topics"] = [Topic(self, **topic) for topic in dct["topics"]]
        if "users" in dct:
            dct["users"] = [User(self, **user) for user in dct["users"]]

        for k, v in dct.items():
            try:
                dct[k] = getattr(self, k)(self, **v)
            except (AttributeError, TypeError):
                continue

        return dct

    def is_admin(self):
        raise NotImplementedError

    # General
    def search(self, term, include_blurbs=True):
        params = {"term": term, "include_blurbs": include_blurbs}
        return self.get("search/query.json", params=params)

    def upload(self, files):
        params = {"files": files}
        response = self.post("uploads.json", params=params)

        return response

    # Categories
    def get_category_list(self):
        return self.get("categories.json")

    def create_category(self, name, color, text_color):
        params = {"name": name, "color": color, "text_color": text_color}
        response = self.post("categories.json", params=params)

        return Category(self, **response["category"])

    # Posts
    def get_latest_posts(self, before):
        # TODO: Figure out good default for before
        params = {"before": before}
        return self.get("posts.json", params=params)

    def get_group_posts(self, group_name):
        return self.get("groups/{}/posts.json".format(group_name))

    def create_post(self, topic_id, raw):
        params = {"topic_id": topic_id, "raw": raw}
        response = self.post("posts.json", params=params)

        return Post(self, **response)

    def get_post_by_number(self, topic_id, post_number):
        response = self.get("posts/by_number/{}/{}.json".format(topic_id, post_number))

        return Post(self, **response)

    def get_post(self, id):
        return self.get("posts/{}.json".format(id))

    # Topics
    def create_topic(self, title, raw, category=None, created_at=None):
        params = {
            "title": title,
            "raw": raw,
            "category": category,
            "created_at": created_at,
        }
        response = self.post("topics.json", params=params)

        return Topic(self, **response)

    def get_topic(self, id, print=False):
        # print=True returns more details, and up to 1000 posts at once.
        # However, it is more heavily rate-limited by default.
        params = {"print": "true"} if print else {}
        response = self.get("t/{}.json".format(id), params=params)

        return Topic(self, **response)

    def get_latest_topics(self, order, ascending=True):
        params = {"order": order, "ascending": ascending}
        return self.get("latest.json", params=params)

    def get_group_topics(self, group_name):
        return self.get("topics/groups/{}.json".format(group_name))

    def get_top_topics(self, flag=""):
        if flag:
            flag = "/{}".format(flag)
        return self.get("top{}.json".format(flag))

    # Invites
    def invite_user(self, email, group_names=None, custom_message=None):
        params = {
            "email": email,
            "group_names": group_names,
            "custom_message": custom_message,
        }
        return self.post("invites", params=params)

    def generate_invite_url(self, email, group_names=None, custom_message=None):
        params = {
            "email": email,
            "group_names": group_names,
            "custom_message": custom_message,
        }
        return self.post("invites/link", params=params)

    # Private Messages
    def create_private_message(self, title, raw, target_usernames, created_at=None):
        params = {
            "title": title,
            "raw": raw,
            "target_usernames": target_usernames,
            "archetype": "private_message",
            "created_at": created_at,
        }
        response = self.post("topics.json", params=params)

        return PrivateMessage(self, **response)

    # Tags
    def get_tag_groups(self):
        return self.get("tag_groups.json")

    def create_tag_group(self, name, tag_names):
        params = {"name": name, "tag_names": tag_names}
        return self.post("tag_groups.json", params=params)

    def get_tag_group(self, id):
        return self.get("tag_groups/{}.json".format(id))

    def update_tag_group(self, id, name, tag_names):
        params = {"name": name, "tag_names": tag_names}
        return self.put("tag_groups/{}.json".format(), params=params)

    def get_tags(self):
        return self.get("tags.json")

    def get_tag(self, tag):
        response = self.get("tags/{}.json".format(tag))
        response["id"] = tag

        return Tag(self, **response)

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

        return self.get(keyword_map[kw].format(kwargs[kw]))

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
        params = {
            "name": name,
            "email": email,
            "password": password,
            "username": username,
            "active": active,
            "approved": approved,
            "user_fields": user_fields,
        }
        response = self.post("users", params=params)

        # Build a user from the input params. Avoids a request.
        params["id"] = response["user_id"]
        response["user"] = User(self, **params)

        return response

    def get_public_users(self, period, order, ascending=True, page=0):
        params = {
            "period": period,
            "order": order,
            "ascending": ascending,
            "page": page,
        }
        return self.get("directory_items.json", params=params)

    def get_users(self, flag, order, ascending=False, page=None, show_emails=None):
        params = {
            "order": order,
            "ascending": ascending,
            "page": page,
            "show_emails": show_emails,
        }
        response = self.get("admin/users/list/{}.json".format(flag), params=params)

        return [User(self, **user) for user in response]

    # Upload

    # Search

    # Admin Emails
    def show_email_settings(self):
        return self.get("admin/email.json")

    def show_email_templates(self):
        return self.get("admin/customize/email_templates.json")

    # Admin

    # Groups
    def get_group(self, name):
        return self.get("groups/{}.json".format(name))

    # Password Reset

    # Site Settings
    def show_site_settings(self):
        # May be able to make an overall "Site Settings" def
        return self.get("admin/site_settings.json")

    # Plugins
    def get_plugins(self):
        response = self.get("admin/plugins")

        return [Plugin(self, **plugin) for plugin in response]

    # Backups
    def get_backups(self):
        return self.get("/admin/backups.json")

    def create_backup(self, with_uploads):
        params = {"with_uploads": with_uploads}
        return self.post("/admin/backups.json", params=params)

    def download_backup(self, filename):
        # TODO: Undocumented response, reverse-engineer it
        return self.put("/admin/backups/{}".format(filename))

    def set_backup_readonly(self, enable):
        # TODO: Documented as empty response. Check it out and return
        #       something useful.
        params = {"enable": enable}
        return self.put("/admin/backups/readonly", params=params)

    # Emails
    def get_emails(self, action, offset):
        # TODO: Offset doesn't appear to be a part of the request syntax.
        #       Need to test and figure out correct request and returns.
        actions = ["sent", "skipped", "bounced", "received", "rejected"]
        actions.remove(action)

        params = {"offset": offset}
        return self.get("/admin/emails/{}.json".format(action), params=params)

    # Flags
    def get_flags(self, type, offset):
        types = ["active", "old"]
        if type not in types:
            raise ValueError('"type" must be one of: {}'.format(types))

        params = {"offset": offset}
        return self.get("/admin/flags/{}.json".format(type), params=params)

    # Badges
    def get_badges(self):
        # TODO: Make a Badge class. Return Badge() list
        return self.get("/admin/badges.json")

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
        params = {
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
        }
        return self.post("/admin/badges.json", params=params)

    # User Fields
    def get_user_fields(self):
        return self.get("/admin/customize/user_fields.json")

    def create_user_field(self, name, description, field_type, required):
        params = {
            "user_field[name]": name,
            "user_field[description]": description,
            "user_field[field_type]": field_type,
            "user_field[required]": required,
        }
        return self.post("/admin/customize/user_fields.json", params=params)

    def delete_user_field(self, id):
        params = {"id": id}
        return self.delete("/admin/customize/user_fields/{id}", params=params)

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
        params = {
            "payload_url": payload_url,
            "content_type": content_type,
            "secret": secret,
            "wildcard_web_hook": wildcard_web_hook,
            "verify_certificate": verify_certificate,
            "active": active,
            "web_hook_event_type_ids": web_hook_event_type_ids,
            "category_ids": category_ids,
            "group_ids": group_ids,
        }
        response = self.post("/admin/api/web_hooks", params=params)

        return WebHook(self, **response)

    # Logs
    def get_staff_action_logs(self, action_name, action_id):
        params = {"action_name": action_name, "action_id": action_id}
        return self.get("/admin/logs/staff_action_logs.json", params=params)

    # About
    def fetch_about(self):
        return self.get("/about.json")

    # Poll Plugin
    def poll_vote(self, post_id, poll_name, options):
        # May be best to implement in Post class. Investigate
        params = {"post_id": post_id, "poll_name": poll_name, "options": options}
        response = self.put("/polls/vote", params=params)

    # Reports
    def get_pageview_stats(self, start_date, end_date, category_id, group_id):
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "category_id": category_id,
            "group_id": group_id,
        }
        return self.get("/page_view_total_reqs", params=params)

    def get_site_configuration(self):
        response = self.get("site.json")

        return response

    def export_report(self, entity, name, start_date, end_date, group_id):
        params = {
            "entity": entity,
            "args[name]": name,
            "args[start_date]": start_date,
            "args[end_date]": end_date,
            "args[group_id]": group_id,
        }
        return self.post("/export_csv/export_entity.json", params=params)
