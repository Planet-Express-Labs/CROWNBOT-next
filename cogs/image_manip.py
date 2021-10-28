import disnake
from disnake import *
from disnake.ext import commands
from utils.regex_patterns import find_url
import ffmpeg
import os


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="tenderize", brief="Makes the image very nice, saturated and tender.",
                            options=[
                                Option("url", "the image you want to tenderize", type=OptionType.string),
                                Option("saturation-amount", "how much to tenderize the image", type=OptionType.integer)
                            ])
    async def cmd_tenderize(self, ctx, url, saturation=10000):
        # if not find_url(url):
        #     return await ctx.response.send_message("I can't find a valid URL. ")
        image = ffmpeg.input(url)
        image = ffmpeg.hue(image, s=saturation)
        ffmpeg.output(image, 'temp.mp4')
        with open('temp.mp4', 'r') as video:
            await ctx.response.send_message("Here's your spicy, tender image:", file=video)
        os.remove('temp.mp4')


def setup(bot):
    bot.add_cog(Images(bot))