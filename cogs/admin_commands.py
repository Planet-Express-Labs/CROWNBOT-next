# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.
from disnake.ext import commands

from utils.admin import admin_command


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="permtest")
    @admin_command
    async def cmdadmin_permtest(self, ctx):
        """
        "You can't see this, and if you can, you shouldn't. " - Liem  (Final last words)
        """
        return await ctx.reply("All your base are belong to us.")


def setup(bot):
    bot.add_cog(Admin(bot))
