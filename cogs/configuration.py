# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not have an issue with it.
import asyncio
from time import sleep

import disnake
from disnake import ApplicationCommandInteraction
from disnake.enums import *
from disnake.ext import commands
from database import databases
from main import __version__
from main import bot
from typing import List


class Menu(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.embed_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True

        # Sets the footer of the embeds with their respective page numbers.
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
    async def first_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.embed_count = 0
        embed = self.embeds[self.embed_count]
        embed.set_footer(text=f"Page 1 of {len(self.embeds)}")

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.next_page.disabled = False
        self.last_page.disabled = False
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.secondary)
    async def prev_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.embed_count -= 1
        embed = self.embeds[self.embed_count]

        self.next_page.disabled = False
        self.last_page.disabled = False
        if self.embed_count == 0:
            self.first_page.disabled = True
            self.prev_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.red)
    async def remove(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(view=None)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.secondary)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.embed_count += 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        if self.embed_count == len(self.embeds) - 1:
            self.next_page.disabled = True
            self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
    async def last_page(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.embed_count = len(self.embeds) - 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        self.next_page.disabled = True
        self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


async def first_time(inter):
    # TODO: FORCE to read from a JSON file.
    embed = disnake.Embed(title="Zoidberg server setup")
    embed.description = """
        Welcome to Zoidberg! I am your new moderation assistant.
        I can automatically delete images that I detect as NSFW, detect spam, and more.
        This wizard will help you configure all of Zoidberg's options.
        I'll update you if we add anything new in your community updates channel.

        Each option screen will have a button that will trigger a settings modal to open.
        If it does not appear, you must update the version of your Discord client.
        
        Press the next button to continue.
        1/4
        """
    await inter.response.send_message(embed=embed)

    embed.description = """
        Would you like to enable image filtering? We use state of the art AI models to detect NSFW images.

        Commonly found NSFW images are stored in a database to reduce load.
        We do not store copies of images that are detected, only a hash that can't be turned back into an image.

        AI Filtering uses advanced AI to detect NSFW images. This includes images containing gore and may falsely 
        detect images of medical procedures. At the moment, this cannot be disabled. This feature will send a copy of 
        any new image, in enabled channels, to our image processing partners. 

        Hash filtering uses our database to detect common images that may not be detected by AI.
        These images usually don't contain nudity, but are still extremely suggestive

        You can configure which channels will use this filter on the next page.
        2/4"""
    await inter.edit_original_message(embed=embed)
    await image_filtering_menu(inter)
    embed.description = """
        I can look for NSFW images in certain channels. By default, I don't scan NSFW channels.
        I also can ignore certain roles.
        
    """


class ConfigModal(disnake.ui.Modal):
    def __init__(self) -> None:
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="The name of the tag",
                custom_id="name",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="The description of the tag",
                custom_id="description",
                style=disnake.TextInputStyle.short,
                min_length=5,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Content",
                placeholder="The content of the tag",
                custom_id="content",
                style=disnake.TextInputStyle.paragraph,
                min_length=5,
                max_length=1024,
            ),
        ]
        super().__init__(title="Create Tag", custom_id="create_tag", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        embed = disnake.Embed(title="Tag Creation")
        for key, value in inter.text_values.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await inter.response.send_message(embed=embed)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        await inter.response.send_message("Oops, something went wrong.", ephemeral=True)


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='setup', brief="Helps you set up Zoidberg to your needs. ")
    async def paginator(self, inter):
        # Creates the embeds as a list.
        embeds = [
            (disnake.Embed(
                title="Welcome to Zoidberg. ",
                description="""
Welcome to Zoidberg! I am your new moderation assistant.
I can automatically delete images that I detect as NSFW, detect spam, and more.
This wizard will help you configure all of Zoidberg's options.
I'll update you if we add anything new in your community updates channel.

Each option screen will have a button that will trigger a settings modal to open.
If it does not appear, you must update the version of your Discord client.

Press the next button to continue.
            """
            ),
                None
            ),
            (disnake.Embed(
                title="Image filtering setup step 1",
                description="""
Would you like to enable image filtering? We use state of the art AI models to detect NSFW images.

Commonly found NSFW images are stored in a database to reduce load.
We do not store copies of images that are detected, only a hash that can't be turned back into an image.

AI Filtering uses advanced AI to detect NSFW images. This includes images containing gore and may falsely 
detect images of medical procedures. At the moment, this cannot be disabled. This feature will send a copy of 
any new image, in enabled channels, to our image processing partners. 

Hash filtering uses our database to detect common images that may not be detected by AI.
These images usually don't contain nudity, but are still extremely suggestive

You can configure which channels will use this filter on the next page.
        """,
                colour=disnake.Color.random(),
            ),
                ConfigModal()
            ),
            disnake.Embed(
                title="Paginator example",
                description="""
I can look for NSFW images in certain channels. By default, I don't scan NSFW channels.
I also can ignore certain roles.
                """,
                colour=disnake.Color.random(),
            ),
        ]

        # Sends first embed with the buttons, it also passes the embeds list into the View class.
        await inter.send(embed=embeds[0], view=Menu(embeds))


def setup(bot):
    bot.add_cog(Configuration(bot))
