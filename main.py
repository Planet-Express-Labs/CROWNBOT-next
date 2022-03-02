# Copyright 2021 Planet Express Labs
# # All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.
import os

import disnake
from disnake.ext import commands
from tortoise import Tortoise
from utils.admin import admin_command
from zoidberg.config import *
import signal
import logging
import sys
import asyncio

__version__ = "3.0 PRE"

activity = disnake.Activity(
    name='> planetexpresslabs.io',
    type=disnake.ActivityType.playing)

# define activity, playing status
# define gateway intents
intents = disnake.Intents.default()
intents.members = True
# TODO: migrate to config
bot = commands.Bot(command_prefix=commands.when_mentioned,
                   activity=activity,
                   intents=intents,
                   test_guilds=[842987183588507670, 769039315945914370])

logging.basicConfig(level=logging.INFO)

print(DISABLED_COGS)
for filename in os.listdir(Path('cogs/')):
    if filename.endswith(".py") and filename not in DISABLED_COGS:
        bot.load_extension(f"cogs.{filename[:-3]}")


async def init():

    # Don't generate schema on first run to prevent wiping DB.
    if os.getenv('PEXL_first_run') is None:
        print("First run detected. Rerun the bot to initialize the DB.")
        os.environ['PEXL_first_run'] = '1'
        print(os.getenv('PEXL_first_run'))
        sys.exit(1)

    if os.getenv("PEXL_first_run") == '1':
        # Generate the schema on first run only
        print("Second/First run detected. Generating schema...")
        os.environ["PEXL_first_run"] = '2'
        await Tortoise.init(
            db_url=CONNURL,
            modules={'models': ['database.databases']},
            _create_db=True
        )
        await Tortoise.generate_schemas()
        return
    if os.getenv("PEXL_force_regen_schema") == '69':
        print("Wiping schema on DB...\nYou asked for it. ")
        await Tortoise.init(
            db_url=CONNURL,
            modules={'models': ['database.databases']},
            _create_db=True
        )
        await Tortoise.generate_schemas(safe=False)
        return

    await Tortoise.init(
        db_url=CONNURL,
        modules={'models': ['database.databases']}
    )


async def handler() -> None:
    """
    Handler for SIGTERM.
    Prevents DB loss by gracefully closing connections.
    """
    print("SIGTERM received. Closing event loops.")
    await bot.close()
    print("Closing DB connections...")
    await Tortoise.close_connections()
    print("DB connections closed. Exiting program. See you soon! Goodbye!")
    sys.exit(1)


# class MainBot(commands.Bot):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(command_prefix=commands.when_mentioned)
#         self.persistent_view = None


@bot.event
async def on_ready():
    # Initialize our databases

    await init()
    await bot.wait_until_ready()
    print(f"Bot is ready, logged in as {bot.user.name} ({bot.user.id}).")


@bot.slash_command(name='foo', description='Tests if the bot is dead or not')
async def cmd_foo(ctx):
    """
    Simple test command
    """
    await ctx.response.send_message(f"Bar!\nLatency: {bot.latency} ms")


@bot.command(name="resetcogs", brief="reloads all the cogs")
@admin_command
async def cmdadmin_resetcogs(ctx: commands.Context):
    """
    Reset all cogs.
    """
    for cog in os.listdir(Path('cogs/')):
        if filename.endswith(".py") and cog not in DISABLED_COGS:
            bot.unload_extension(cog)
            bot.load_extension(cog)
    await ctx.message.delete()
    await ctx.send("Cogs reset.", delete_after=5)

# Gracefully handle Heroku's SIGTERM signal to prevent DB data loss.
signal.signal(signal.SIGTERM, handler)


bot.run(BOT_TOKEN)
