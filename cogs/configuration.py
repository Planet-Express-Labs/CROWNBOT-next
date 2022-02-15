# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not have an issue with it.

from typing import List
from tortoise import Tortoise
import disnake
from disnake.ext import commands
import re


class Menu(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.embed_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.additional_components = []

        # Sets the footer of the embeds with their respective page numbers.
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")
            terms = re.findall(r"%([^;]*)", embed.description)
            if any(terms):
                embed.description = embed.description.replace(f"%{terms[0]}", "")
                for each in terms:
                    if each[0:7] == "%TOGGLE":
                        params = each.replace('(', '').replace(')', '').split(', ')
                        models = Tortoise.describe_models()
                        for model in models:
                            name = model.__name__
                            if name.lower == params[0]:
                                break

                        self.additional_components.append(
                            disnake.ui.Button(
                                label=params[2],
                                custom_id=params[3]
                            )
                        )

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
    async def first_page(self, interaction: disnake.MessageInteraction):
        self.embed_count = 0
        embed = self.embeds[self.embed_count]
        embed.set_footer(text=f"Page 1 of {len(self.embeds)}")

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.next_page.disabled = False
        self.last_page.disabled = False
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="◀")
    async def prev_page(self, interaction: disnake.MessageInteraction):
        self.embed_count -= 1
        embed = self.embeds[self.embed_count]

        self.next_page.disabled = False
        self.last_page.disabled = False
        if self.embed_count == 0:
            self.first_page.disabled = True
            self.prev_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.red)
    async def remove(self, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(view=None)

    @disnake.ui.button(emoji="▶")
    async def next_page(self, interaction: disnake.MessageInteraction):
        self.embed_count += 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        if self.embed_count == len(self.embeds) - 1:
            self.next_page.disabled = True
            self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
    async def last_page(self, interaction: disnake.MessageInteraction):
        self.embed_count = len(self.embeds) - 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        self.next_page.disabled = True
        self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='setup', description="Helps you set up Zoidberg to your needs. ")
    async def paginator(self, inter):
        # Creates the embeds as a list.
        embeds = [
            disnake.Embed(
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
            disnake.Embed(
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
%TOGGLE(Server, image_filtering, enable_image_filtering)
%TOGGLE(Server, hash_filtering, enable_image_filtering)
        """,
                colour=disnake.Color.random(),
            ),
            disnake.Embed(
                title="Paginator example",
                description="""
I can look for NSFW images in certain channels. By default, I don't scan NSFW channels.
I also can ignore certain roles.
%MODAL(ConfigRoleModal)
                """,
                colour=disnake.Color.random(),
            )
        ]

        # Sends first embed with the buttons, it also passes the embeds list into the View class.
        await inter.send(embed=embeds, view=Menu(embeds))


def setup(bot):
    bot.add_cog(Configuration(bot))
