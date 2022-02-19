import inspect
import secrets
import logging
from asyncio import TimeoutError
from math import floor
from zoidberg.config import *


def verify_user(ctx):
    for each in ADMIN_ID:
        print(ADMIN_ID, ctx.message.author.id)
        return int(ctx.message.author.id) == int(each)


def admin_command(func):
    async def wrapper(*args, **kwargs):
        if inspect.ismethod(func):
            ctx = args[1]
        else:
            ctx = args[0]
        bot = ctx.bot
        logging.info(
            ctx.message.author.name,
            "is trying to use an admin command. ",
            func.__name__)
        if verify_user(ctx):
            message = await ctx.send("""```
We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

root's one time password (sent in the console):
            ```""")
            otp = secrets.token_urlsafe(6)
            print(ctx.message.author.name + "'s otp code", otp)

            def wait(m):
                if m.channel.id == ctx.channel.id and m.author.id == ctx.author.id:
                    return m.content
            try:
                resp = await bot.wait_for('message', check=wait)
            except TimeoutError:
                return await bot.response.send_message("The verification has timed out. Please try again.",
                                                       delete_after=5)
            await message.delete()
            if int(resp.content) == otp:
                await ctx.send("You have been verified.", delete_after=5)
                await resp.delete()
                return await func(*args, **kwargs)
            else:
                return await ctx.send("The verification code you entered was incorrect. Please try again.",
                                      delete_after=5)
        else:
            return await ctx.send("You do not have permission to use this command.",
                                  delete_after=5)
    return wrapper
