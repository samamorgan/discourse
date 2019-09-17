import requests

from .category import Category
from .invite import Invite
from .notification import Notification
from .plugin import Plugin
from .post import Post
from .private_message import PrivateMessage
from .tag import Tag
from .topic import Topic
from .user import User


class Client(object):

    Category = Category
    Invite = Invite
    Notification = Notification
    Plugin = Plugin
    Post = Post
    PrivateMessage = PrivateMessage
    Tag = Tag
    Topic = Topic
    User = User

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
            return True
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
        archetype = 'private_message'
        pass

    # Notifications

    # Tags

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

    # Admin

    # Groups

    # Password Reset

    # Site Settings

    # Plugins

    # Backups

    # Emails

    # Flags

    # Badges

    # User Fields

    # Web Hooks

    # Logs

    # About

    # Poll Plugin

    # Reports
