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
            'api_username': api_username,
            'api_key': api_key
        })

    # Class Methods
    def _request(self, method, path, params=None, data=None):
        response = self.session.request(
            method=method.upper(),
            url='{}/{}'.format(self.host, path),
            params=params,
        )

        return response

    # General
    def search(self, term, include_blurbs=True):
        response = self._request('GET', 'search/query.json', params={
            'term': term,
            'include_blurbs': include_blurbs,
        })

        return response

    # Categories
    def get_category_list(self):
        response = self._request('GET', 'categories.json')

        categories = []
        for category in response['category_list']['categories']:
            categories.append(self.Category(self, category))

        return categories

    def create_category(self, name, color, text_color):
        return Category()

    # Posts
    def get_latest_posts(self, before):
        return [Post(), Post()]

    def create_post(self):
        return Post()

    def get_post(self, id):
        return Post(id)

    # Topics
    def create_topic(self, title, raw, category=None, created_at=None):
        return Topic()

    def get_topic(self, id):
        return Topic()

    def get_latest_topics(self, order, ascending=True):
        return [Topic(), Topic()]

    def get_top_topics(self, flag=''):
        return [Topic(), Topic()]

    def create_timed_topic(
        self,
        time,
        status_type,
        based_on_last_post,
        category_id
    ):
        return

    # Invites

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
    def get_user(self, id, usename=None, external_id=None):
        return User() or None

    def create_user(
        self,
        name,
        email,
        password,
        username,
        active,
        approved,
        user_fields
    ):
        return User() or None

    def get_public_users(self, period, order, ascending=True, page=0):
        return [User(), User()]

    # Upload

    # Search

    # Admin Emails

    # Admin

    # Groups

    # Password Reset

    # Site
    def get_site(self):
        response = self._request('GET', 'categories.json')

        return self.Category(self, response)

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
