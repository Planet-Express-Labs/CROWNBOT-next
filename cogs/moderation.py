# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not have an issue with it.
import disnake
from disnake.ext import commands
from disnake import Option, OptionType


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        brief="Gets user info",
        options=[
            Option("user", "User to get info for.", OptionType.user, required=True)
        ],
        name="user-info"
    )
    async def user_info(self, ctx, user=None):
        badges = {
            "staff": "<:staff:812692120049156127>",
            "partner": "<:partner:812692120414322688>",
            "hypesquad": "<:hypesquad_events:812692120358879262>",
            "bug_hunter": "<:bug_hunter:812692120313266176>",
            "hypesquad_bravery": "<:bravery:812692120015339541>",
            "hypesquad_brilliance": "<:brilliance:812692120326373426>",
            "hypesquad_balance": "<:balance:812692120270798878>",
            "verified_bot_developer": "<:verified_bot_developer:812692120133042178>"
        }

        badge_string = ' '.join(badges[pf.name] for pf in user.public_flags.all() if pf.name in badges)
        created_at = str(user.created_at)[:-7]
        reply = disnake.Embed(color=disnake.Color.blurple())
        reply.title = str(user)
        reply.set_thumbnail(url=user.display_avatar)
        reply.add_field(
            name="Registration",
            value=(
                f"⌚ **Created at:** `{created_at}`\n"
                f"📋 **ID:** `{user.id}`"
            ),
            inline=False
        )
        if len(badge_string) > 1:
            reply.add_field(
                name="Badges",
                value=f"`->` {badge_string}"
            )
        await ctx.response.send_message(embed=reply)

    @commands.has_permissions(manage_messages=True)
    @commands.slash_command(
        name="embed",
        description="Creates an embed",
        options=[
            Option("channel", "Where the message should be sent.", OptionType.channel),
            Option("title", "Creates a title", OptionType.string),
            Option("description", "Creates a description", OptionType.string),
            Option("color", "Colors the embed", OptionType.string),
            Option("image_url", "URL of the embed's image", OptionType.string),
            Option("footer", "Creates a footer", OptionType.string),
            Option("footer_url", "URL of the footer image", OptionType.string)
        ]
    )
    async def embed(self, ctx, channel=None, title=None, description=None, color=None, image_url=None, footer=None,
                    footer_url=None):
        if color is not None:
            color = await commands.ColorConverter().convert(ctx, color)
        else:
            color = disnake.Color.default()
        embed = disnake.Embed(color=color)
        if title is not None:
            embed.title = title
        if description is not None:
            embed.description = description
        if image_url is not None:
            embed.set_image(url=image_url)
        footer_args = {}
        if footer is not None:
            footer_args['text'] = footer
        if footer_url is not None:
            footer_args['icon_url'] = footer_url
        if footer_args:
            embed.set_footer(**footer_args)
        if channel is None:
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.response.send_message("Sent!")
            await channel.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.slash_command(
        name="ban",
        description="Ban user",
        options=[
                Option("user", "User to ban", OptionType.user, required=True),
                Option("purge", "Number of days to purge messages. ", OptionType.string),
                Option("reason", "Reason for the ban", OptionType.string)
                ]
    )
    async def ban(self, ctx, user, reason=None, purge=0):
        try:
            await ctx.guild.ban(user=user, reason=reason, delete_message_days=purge)
            await ctx.response.send_message(f"Success! {user.name} has been banned. ")
        except disnake.errors.Forbidden:
            await ctx.response.send_message(f"I do not have permission to execute this command!")

    @commands.has_permissions(manage_messages=True)
    @commands.slash_command(
        name="purge",
        description="Deletes a lot of messages. How many messages? A lot!",
        options=[
            Option("limit", "Number of messages to delete", OptionType.integer, required=True),
            Option("user", "Who's messages to delete", OptionType.user),
            Option("channel", "Channel from which to delete the messages.", OptionType.channel)
        ]
    )
    async def purge(self, ctx, limit, user=None, channel=None):
        if channel is None:
            channel = ctx.channel
        messages = []
        if user is None:
            await channel.purge(limit=limit)
        else:
            async for message in channel.history():
                if len(messages) == limit:
                    break
                if message.author == user:
                    messages.append(message)
            await channel.delete_messages(messages)
        await ctx.response.send_message(f"Deleted {limit} messages from {channel.mention}.", ephemeral=True)

    @commands.has_permissions(kick_members=True)
    @commands.slash_command(
        name="kick",
        description="Kick user",
        options=[Option("user", "User to kick", OptionType.user, required=True)]
    )
    async def kick(self, ctx, user):
        try:
            await user.kick()
            await ctx.response.send_message(f"{user.mention} has been kicked successfully.")
        except disnake.errors.Forbidden:
            await ctx.response.send_message(f"I do not have permission to execute this command!")


def setup(bot):
    bot.add_cog(Moderation(bot))
