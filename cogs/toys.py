# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.

import art
import disnake
from disnake.ext import commands
from PIL import Image
from utils import images
import io

class Toys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="big-text",
                            description="Makes the text a big boy!.")
    async def cmd_big_text(self, inter, text: str = commands.Param(),
                           font: str = commands.Param(desc='Python Art text2art supported fonts.', default='ascii')):
        """
        big boy textifer
        :Context inter:
        :string text:
        """
        try:
            await inter.response.send_message(f"```{art.text2art(text, font=font)}```")
        except art.artError:
            await inter.response.send_message(f":exclamation: Something went wrong! Are you sure {font} exists within text2art?")

    @commands.slash_command(name="ascii-art",
                            description="Converts content to ASCII art.")
    async def cmd_text_to_art(self, inter,
                              image: disnake.Attachment = commands.Param(),
                              columns: int = commands.Param(default=80)) -> None:
        """
        Converts text to ASCII art.
        :param image: image to convert to ASCII art
        :param text: text to convert to ASCII art
        :param inter:
        :return:
        """
        byte = await image.read()
        img = Image.open(io.BytesIO(byte))
        ascii = images.image_to_ascii(img, columns=columns)
        if len(ascii) > 4000:
            return await inter.response.send_message(f"```{ascii}```")
        else:
            return await inter.response.send_message("The size of the image is too large for me to send as a "
                                                     "message!", file=disnake.File(bytes(ascii), "result.txt"))


def setup(bot):
    bot.add_cog(Toys(bot))
