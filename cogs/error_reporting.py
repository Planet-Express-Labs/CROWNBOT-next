# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.
import disnake
from disnake.ext import commands
from zoidberg.config import error_channel


class Reporting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="report-error")
    async def report_error(self, ctx, *, error_message):
        """Report an error to the bot owner."""
        embed = disnake.Embed(
            title="User reported error",
            description=error_message)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Triggered by report-error")
        await ctx.send(f"{ctx.author.mention} Your error has been reported.")
        await ctx.bot.get_channel(error_channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        embed = disnake.Embed(
            title="Bot on",
            description="Bot is now online. ")
        await self.bot.get_channel(error_channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Triggered when something breaks while executing a command."""
        if not isinstance(error, commands.CommandNotFound):
            embed = disnake.Embed(
                title="Command error",
                description=str(error))
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar_url)
            embed.set_footer(text="Triggered by command error")
            await ctx.bot.get_channel(error_channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.AppCmdInter, error: commands.CommandError):
        """Triggered when something breaks while executing a slash command."""
        embed = disnake.Embed(
            title="Slash command error",
            description=str(error))
        embed.set_author(
            name=inter.author.name,
            icon_url=inter.author.avatar_url)
        embed.set_footer(text="Triggered by slash command error")
        await inter.bot.get_channel(error_channel).send(embed=embed)


def setup(bot):
    bot.add_cog(Reporting(bot))
