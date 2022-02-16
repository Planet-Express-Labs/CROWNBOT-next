# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.
from disnake.ext import commands
import disnake

from database.databases import *
from utils.integrations import *
from utils.integrations.azure_cm import image_moderation


class TextModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        server = await Server.find_all(Server.server_id == message.guild.id)
        if server.filter_long_text:
            if len(message.content) > server.filter_long_text_limit:
                await message.delete()


class ImageFiltering(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        """
        This listener sends all images to our AI providers to get scanned for nsfw content.

        For now, this just uses Azure Cognitive Services, but more will be trained in the future.
        """
        server = await Server.find_all(Server.server_id == message.guild.id)
        if not server.filter_images or not message.attachments:
            return

        permissions = server.image_filtering_roles
        if permissions is not None:
            for each in message.author.permissions_in(message.channel):
                if each in permissions:
                    return

        channels = server.image_filtering_channels
        for each in channels:
            if message.channel.id == server.image_filtering_channels_blocklist:
                return

        if message.author.id != self.bot.id:
            for attachment in message.attachments:
                az_result = image_moderation(attachment.url)


def setup(bot):
    bot.add_cog(TextModeration(bot))
