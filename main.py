# Copyright 2021 Planet Express Labs
# # All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not have an issue with it.
import disnake
from disnake.ext import commands
from tortoise import Tortoise
from utils.admin import admin_command
from zoidberg.config import *

__version__ = "3.0 PRE"

# define activity, playing status
activity = disnake.Activity(name='> planetexpresslabs.io', type=disnake.ActivityType.playing)
# define gateway intents
intents = disnake.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned,
                   activity=activity,
                   intents=intents,
                   # TODO place this the config file once again.
                   test_guilds=[842987183588507670])

logging.basicConfig(level=logging.INFO)
for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename not in DISABLED_COGS:
        bot.load_extension(f"cogs.{filename[:-3]}")

async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url=CONNURL,
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
        
    
@bot.event
async def on_ready():
    # Initialize our databases
    await init()
    print(f"Bot is ready, logged in as {bot.user.name} ({bot.user.id}).")
    await bot.wait_until_ready()


@bot.slash_command(name='foo', brief='Tests if the bot is dead or not')
async def cmd_foo(ctx):
    await ctx.response.send_message(f"Bar!\nLatency: {bot.latency} ms")


@bot.command(name="resetcogs")
@admin_command
async def cmdadmin_resetcogs(ctx):
    """
    Reset all cogs.
    """
    for cog in bot.cogs:
        if cog not in DISABLED_COGS:
            bot.unload_extension(cog)
            bot.load_extension(cog)
    return await ctx.reply("Cogs reset.")


bot.run(BOT_TOKEN)
