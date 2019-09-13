from .category import Category
from .post import Post
from .topic import Topic
from .user import User


class Client(object):

    def __init__(self, host, api_username, api_key):
        self.host = host
        self.api_username = api_username
        self.api_key = api_key

    # CATEGORIES
    def get_category_list(self):
        return [Category(), Category()]

    def create_category(self, name, color, text_color):
        return Category()

    def get_category_topics(self, id, page):
        return [Topic(), Topic()]

    def update_category(self, name, color, text_color):
        return Category()

    # POSTS
    def get_latest_posts(self, before):
        return [Post(), Post()]

    def create_post(self):
        return Post()

    def create_private_message(self):
        pass

    def get_post(self, id):
        return Post(id)

    def update_post(self, id, raw, raw_old, edit_reason, cooked):
        return Post()

    def lock_post(self, id):
        return True or False

    def post_action(self, action):
        return Post(), True or False

    # TOPICS
    def create_topic(self, title, raw, category=None, created_at=None):
        return Topic()

    def get_topic(self, id):
        return Topic()

    def get_latest_topics(self, order, ascending=True):
        return [Topic(), Topic()]

    def get_top_topics(self, flag=''):
        return [Topic(), Topic()]

    def create_timed_topic(self, time, status_type, based_on_last_post, category_id):
        return

    # INVITES

    # PRIVATE MESSAGES

    # NOTIFICATIONS

    # TAGS

    # USERS
    def get_user(self, id, usename=None, external_id=None):
        return User() or None

    def create_user(self, name, email, password, username, active, approved, user_fields):
        return User() or None

    def get_public_users(self, period, order, ascending=True, page=0):
        return [User(), User()]

    # UPLOAD

    # SEARCH

    # ADMIN EMAILS

    # ADMIN

    # GROUPS

    # PASSWORD RESET

    # SITE SETTINGS

    # PLUGINS

    # BACKUPS

    # EMAILS

    # FLAGS

    # BADGES

    # USER FIELDS

    # WEB HOOKS

    # LOGS

    # ABOUT

    # POLL PLUGIN

    # REPORTS
