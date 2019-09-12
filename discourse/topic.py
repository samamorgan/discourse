class Topic(object):
    def __init__(self, id):
        self.id = id
        self.post_stream: {
            'posts': [],
            'stream': []
        }
        self.timeline_lookup = [{}]
        self.id = 0
        self.title = ''
        self.fancy_title = ''
        self.posts_count = 0
        self.created_at = ''
        self.views = 0
        self.reply_count = 0
        self.participant_count = 0
        self.like_count = 0
        self.last_posted_at = {}
        self.visible = True
        self.closed = True
        self.archived = True
        self.has_summary = True
        self.archetype = ''
        self.slug = ''
        self.category_id = 0
        self.word_count = {}
        self.deleted_at = {}
        self.user_id = 0
        self.draft = {}
        self.draft_key = ''
        self.draft_sequence = {}
        self.unpinned = {}
        self.pinned_globally = True
        self.pinned = True
        self.pinned_at = ''
        self.pinned_until = {}
        self.details: {
            'auto_close_at': {},
            'auto_close_hours': {},
            'auto_close_based_on_last_post': True,
            'created_by': {},
            'last_poster': {},
            'participants': [],
            'suggested_topics': [],
            'notification_level': 0,
            'can_flag_topic': True,
        }
        self.highest_post_number: 0
        self.deleted_by: {}
        self.actions_summary: [{}]
        self.chunk_size: 0
        self.bookmarked: {}

    def get_post(self):
        return

    def remove(self, id):
        return True or False

    def update(self, id, slug='-'):
        return Topic()

    def invite_user(self, id, user):
        return True or False

    def bookmark(self, id):
        return

    def update_status(self, id, status, enabled, until):
        return

    def update_timestamp(self, timestamp):
        return True or False

    def set_notification_level(self, notification_level):
        return True or False
