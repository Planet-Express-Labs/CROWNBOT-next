from tortoise.models import Model
from tortoise import fields


class Server(Model):
    server_id = fields.BigIntField(pk=True)
    preferred_name = fields.StringField(max_length=255, default="")
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
    filter_long_text_limit = fields.IntegerField(default=100, null=True)


class User(Model):
    user_id = fields.BigIntField(pk=True)
    preferred_name = fields.StringField(max_length=255, default="")
    premium = fields.BooleanField(default=False)
    pronouns = fields.TextField(default="", null=True)
    gender = fields.TextField(default="", null=True)
    birthday = fields.DatetimeField(default="", null=True)
    private = fields.BooleanField(default=False)


class ConfessChannel(Model):
    confess_id = fields.IntField(pk=True)
    enable = fields.BooleanField(default=False, null=True)
    guild = fields.BigIntField(default=0, null=True)
    confess_channel = fields.BigIntField(default=0)
    log_channel = fields.BigIntField(default=0, null=True)
    last_confess = fields.BigIntField(default=0, null=True)
    blocked_users = fields.TextField(default="", null=True)
    whitelist = fields.BooleanField(default=False, null=True)
    allowed_roles = fields.TextField(default="", null=True)


