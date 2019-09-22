import requests

from .category import Category
from .plugin import Plugin
from .post import Post
from .private_message import PrivateMessage
from .tag import TagGroup, Tag
from .topic import Topic
from .user import User


class Client(object):

    def __init__(self, host, api_username, api_key):
        self.host = host

        self.session = requests.Session()
        self.session.headers.update({
            'Api-Username': api_username,
            'Api-Key': api_key
        })

    # Class Methods
    def _request(self, method, path, params=None, data=None):
        response = self.session.request(
            method=method.upper(),
            url='{}/{}'.format(self.host, path),
            params=params,
            data=data,
        )

        if not response.ok:
            response.raise_for_status()

        return response.json()

    # General
    def search(self, term, include_blurbs=True):
        # TODO: Parse json and pass back an array of objects
        response = self._request('GET', 'search/query.json', params={
            'term': term,
            'include_blurbs': include_blurbs,
        })

        return response

    def upload(files):
        # TODO: Reverse-engineer this request
        raise NotImplementedError

    # Categories
    def get_category_list(self):
        response = self._request('GET', 'categories.json')

        return [
            Category(client=self, json=category)
            for category
            in response['category_list']['categories']
        ]

    def create_category(self, name, color, text_color):
        response = self._request('POST', 'categories.json', params={
            'name': name,
            'color': color,
            'text_color': text_color,
        })

        return Category(client=self, json=response['category'])

    # Posts
    def get_latest_posts(self, before):
        # TODO: Figure out good default for before
        response = self._request('GET', 'posts.json', params={
            'before': before
        })

        return [
            Post(client=self, json=post)
            for post
            in response['latest_posts']
        ]

    def create_post(self, topic_id, raw):
        response = self._request('POST', 'posts.json', params={
            'topic_id': topic_id,
            'raw': raw,
        })

        return Post(client=self, json=response)

    def get_post(self, id):
        response = self._request('GET', 'posts/{}.json'.format(id))

        return Post(client=self, json=response)

    # Topics
    def create_topic(self, title, raw, category=None, created_at=None):
        response = self._request('POST', 'topics.json', params={
            'title': title,
            'raw': raw,
            'category': category,
            'created_at': created_at,
        })

        return Topic(client=self, json=response)

    def get_topic(self, id):
        response = self._request('GET', 't/{}.json'.format(id))

        return Topic(client=self, json=response)

    def get_latest_topics(self, order, ascending=True):
        response = self._request('GET', 'latest.json', params={
            'order': order,
            'ascending': ascending,
        })

        return [
            Topic(client=self, json=topic)
            for topic
            in response['topic_list']['topics']
        ]

    def get_top_topics(self, flag=''):
        if flag:
            flag = '/{}'.format(flag)
        response = self._request('GET', 'top{}.json'.format(flag))

        return [
            Topic(client=self, json=topic)
            for topic
            in response['topic_list']['topics']
        ]

    # Invites
    def invite_user(self, email, group_names=None, custom_message=None):
        response = self._request(
            'POST',
            'invites',
            params={
                'email': email,
                'group_names': group_names,
                'custom_message': custom_message
            }
        )

        if response['success'] == 'OK':
            return User(client=self, json=response['user'])
        return False

    def generate_invite_url(
        self,
        email,
        group_names=None,
        custom_message=None
    ):
        response = self._request(
            'POST',
            'invites/link',
            params={
                'email': email,
                'group_names': group_names,
                'custom_message': custom_message
            }
        )

        return response

    # Private Messages
    def create_private_message(
        self,
        title,
        raw,
        target_usernames,
        created_at=None
    ):
        response = self._request('POST', 'topics.json', params={
            'title': title,
            'raw': raw,
            'target_usernames': target_usernames,
            'archetype': 'private_message',
            'created_at': created_at,
        })

        return PrivateMessage(client=self, json=response)

    # Tags
    def get_tag_groups(self):
        response = self._request('GET', 'tag_groups.json')

        return [
            TagGroup(client=self, json=tag_group)
            for tag_group
            in response['tag_groups']
        ]

    def create_tag_group(self, name, tag_names):
        response = self._request('POST', 'tag_groups.json', params={
            'name': name,
            'tag_names': tag_names,
        })

        return TagGroup(client=self, json=response['tag_group'])

    def get_tag_group(self, id):
        response = self._request('GET', 'tag_groups/{}.json'.format(id))

        return TagGroup(client=self, json=response['tag_group'])

    def update_tag_group(self, id, name, tag_names):
        response = self._request(
            'PUT',
            'tag_groups/{}.json'.format(),
            params={'name': name, 'tag_names': tag_names}
        )

        return TagGroup(client=self, json=response['tag_group'])

    def get_tags(self):
        response = self._request('GET', 'tags.json')
        return [Tag(client=self, json=tag) for tag in response['tags']]

    def get_tag(self, tag):
        response = self._request('GET', 'tags/{}.json'.format(tag))
        response['id'] = tag

        return Tag(client=self, json=response)

    # Users
    def get_user(self, **kwargs):
        keyword_map = {
            'id': 'admin/users/{}.json',
            'username': 'users/{}.json',
            'external_id': 'u/by-external/{}.json',
        }
        if len(kwargs) != 1:
            raise TypeError(
                'get_user() takes 1 keyword argument but {} were given'.format(
                    len(kwargs)
                )
            )

        kw = list(kwargs)[0]
        if kw not in keyword_map:
            raise TypeError(
                '"{}" is not a valid keyword argument.'.format(kw)
            )

        response = self._request(
            'GET',
            keyword_map[kw].format(kwargs[kw])
        )

        if kw == 'id':
            return User(client=self, json=response)
        return User(client=self, json=response['user'])

    def create_user(
        self,
        name,
        email,
        password,
        username,
        active=True,
        approved=True,
        user_fields=''
    ):
        response = self._request('POST', 'users', params={
            'name': name,
            'email': email,
            'password': password,
            'username': username,
            'active': active,
            'approved': approved,
            'user_fields': user_fields,
        })

        return self.get_user(id=response['user_id'])

    def get_public_users(self, period, order, ascending=True, page=0):
        response = self._request('GET', 'directory_items.json', params={
            'period': period,
            'order': order,
            'ascending': ascending,
            'page': page,
        })

        # TODO: Return more than just the users here
        return [
            User(client=self, json=user)
            for user
            in response['directory_items']['user']
        ]

    def get_users(
        self,
        flag,
        order,
        ascending=True,
        page=None,
        show_emails=None,
    ):
        response = self._request(
            'GET',
            'admin/users/list/{}.json'.format(self.flag),
            params={
                'order': order,
                'ascending': ascending,
                'page': page,
                'show_emails': show_emails,
            }
        )

        return [User(client=self, json=user) for user in response]

    # Upload

    # Search

    # Admin Emails
    def show_email_settings(self):
        raise NotImplementedError

    def show_email_templates(self):
        raise NotImplementedError

    # Admin

    # Groups
    def create_group(self, name):
        raise NotImplementedError

    def get_groups(self):
        raise NotImplementedError

    def get_group(self, name):
        raise NotImplementedError

    # Password Reset

    # Site Settings
    def show_site_settings(self):
        # May be able to make an overall "Site Settings" def
        raise NotImplementedError

    # Plugins
    def get_plugins(self):
        response = self._request('GET', 'admin/plugins')

        return [Plugin(client=self, json=plugin) for plugin in response]

    # Backups
    def get_backups(self):
        raise NotImplementedError

    def create_backup(self, with_uploads):
        raise NotImplementedError

    def download_backup(self, filename):
        raise NotImplementedError

    def set_backup_readonly(self, enable=True):
        raise NotImplementedError

    # Emails
    def get_emails(self, action, offset):
        raise NotImplementedError

    # Flags
    def get_flags(self, type, offset):
        raise NotImplementedError

    # Badges
    def get_badges(self):
        raise NotImplementedError

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
        raise NotImplementedError

    # User Fields
    def get_user_fields(self):
        raise NotImplementedError

    def create_user_field(self, name, description, field_type, required):
        raise NotImplementedError

    def delete_user_field(self, id):
        raise NotImplementedError

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
        raise NotImplementedError

    # Logs
    def get_staff_action_logs(self):
        raise NotImplementedError

    # About
    def fetch_about(self):
        raise NotImplementedError

    # Poll Plugin
    def poll_vote(self, post_id, poll_name, options):
        # May be best to implement in Post class. Investigate
        raise NotImplementedError

    # Reports
    def get_pageview_stats(self, start_date, end_date, category_id, group_id):
        raise NotImplementedError

    def export_report(self, entity, name, start_date, end_date, group_id):
        raise NotImplementedError
