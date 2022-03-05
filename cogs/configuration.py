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

    


def setup(bot):
    bot.add_cog(Configuration(bot))
