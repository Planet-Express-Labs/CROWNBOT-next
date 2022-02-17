# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.


import disnake
from disnake.ext import commands


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='setup',
                            description="Helps you set up Zoidberg to your needs. ")
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
%TOGGLE(Server, image_filtering, enable image filtering);
%TOGGLE(Server, hash_filtering, enable image filtering);
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

        # Sends first embed with the buttons, it also passes the embeds list
        # into the View class.
        await inter.send(embed=embeds, view=Menu(embeds))


def setup(bot):
    bot.add_cog(Configuration(bot))
