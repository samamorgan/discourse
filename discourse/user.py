class User(object):
    def __init__(self, id):
        self.id = id
        self.id = 0
        self.username = ''
        self.avatar_template = ''
        self.name = {}
        self.last_posted_at = ''
        self.last_seen_at = ''
        self.created_at = ''
        self.website_name = {}
        self.can_edit = True
        self.can_edit_username = True
        self.can_edit_email = True
        self.can_edit_name = True
        self.can_send_private_messages = True
        self.can_send_private_message_to_user = True
        self.trust_level = 0
        self.moderator = True
        self.admin = True
        self.title = {}
        self.uploaded_avatar_id = {}
        self.badge_count = 0
        self.custom_fields = {}
        self.pending_count = 0
        self.profile_view_count = 0
        self.primary_group_name = {}
        self.primary_group_flair_url = {}
        self.primary_group_flair_bg_color = {}
        self.primary_group_flair_color = {}
        self.invited_by = {}
        self.groups = []
        self.featured_user_badge_ids = []
        self.card_badge = {}

    def update_avatar(self, upload_id, type):
        return True or False

    def update_email(self, email):
        return True or False

    def delete(self):
        return True or False

    def log_out(self):
        return True or False

    def refresh_gravatar(self):
        return True or False
