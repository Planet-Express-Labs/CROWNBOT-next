from tortoise.models import Model
from tortoise import fields


class Server(Model):
    server_internal_id = fields.IntField(pk=True)
    server_id = fields.BigIntField()
    preferred_name = fields.TextField(max_length=255, default="")
    roles = fields.TextField(default="", null=True)
    premium = fields.BooleanField(default=False, null=True)

    # Image filtering
    image_filtering = fields.BooleanField(default=False, null=True)
    image_filtering_channels = fields.TextField(default="", null=True)
    image_filtering_blocklist = fields.BooleanField(default=False, null=True)
    image_filtering_roles = fields.TextField(default="", null=True)
    image_filtering_blocklist_roles = fields.BooleanField(default=False, null=True)
    image_filtering_nsfw = fields.BooleanField(default=True, null=True)

    filter_long_text = fields.BooleanField(default=False, null=True)
    filter_long_text_limit = fields.IntField(default=100, null=True)

    def __str__(self):
        return self.preferred_name

    class Meta:
        table = "servers"


class Logging(Model):
    """
    Logging settings for a server, mostly unused for the current moment.
    """
    server_internal_id = fields.IntField(pk=True)
    server_id = fields.BigIntField()
    logging_enabled = fields.BooleanField(default=False, null=True)
    logging_channel = fields.BigIntField()

    # Message state
    message_state_channel = fields.BigIntField()
    deleted_message = fields.BooleanField(default=False)
    edited_message = fields.BooleanField(default=False)

    # User state
    user_state_channel = fields.BigIntField()
    user_joined = fields.BooleanField(default=False)
    user_left = fields.BooleanField(default=False)
    user_banned = fields.BooleanField(default=False)
    user_unbanned = fields.BooleanField(default=False)
    user_muted = fields.BooleanField(default=False)
    user_unmuted = fields.BooleanField(default=False)
    user_nickname_changed = fields.BooleanField(default=False)
    user_roles_changed = fields.BooleanField(default=False)
    user_avatar_changed = fields.BooleanField(default=False)

    # Announcement logging
    announcement_channel = fields.BigIntField()
    announcements_enabled = fields.BooleanField(default=False)
    user_joined_announcement = fields.BooleanField(default=False)
    user_joined_announcement_message = fields.JSONField(default="")

    class Meta:
        table = "logging"


class Reminder(Model):
    reminder_id = fields.IntField(pk=True)
    reminder_name = fields.TextField(max_length=255, default="")
    server_id = fields.BigIntField()
    channel_id = fields.BigIntField()
    user_id = fields.BigIntField()
    dm = fields.BooleanField()
    ping = fields.BooleanField(default=False)
    created = fields.DatetimeField(auto_now_add=True)
    metadata = fields.JSONField()

    def __str__(self):
        return self.reminder_name

    class Meta:
        table = "reminders"


class User(Model):
    # Stores information that is used to personalize settings on a specific user
    # Also provides a way for the bot to generate a profile for a user with features that discord doesn't provide
    user_internal_id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    preferred_name = fields.TextField(max_length=255, null=True)
    premium = fields.BooleanField(default=False)
    pronouns = fields.TextField(null=True)
    gender = fields.TextField(null=True)
    birthday = fields.DatetimeField(null=True)
    private = fields.BooleanField(default=False)

    def __str__(self):
        return self.preferred_name

    class Meta:
        table = "users"


class ConfessChannel(Model):
    # Stores information specific to confess channels
    intenral_id = fields.IntField(pk=True)
    confess_id = fields.BigIntField()
    enable = fields.BooleanField(default=False, null=True)
    guild = fields.BigIntField(default=0, null=True)
    confess_channel = fields.BigIntField(default=0)
    log_channel = fields.BigIntField(default=0, null=True)
    last_confess = fields.BigIntField(default=0, null=True)
    blocked_users = fields.TextField(default="", null=True)
    whitelist = fields.BooleanField(default=False, null=True)
    allowed_roles = fields.TextField(default="", null=True)

    def __str__(self):
        return str(self.confess_id)

    class Meta:
        table = "confess_channels"
