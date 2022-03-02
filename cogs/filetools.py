import pypdftk
from disnake.ext import commands


def flatten_pdf(attachment):
    pypdftk.fill_form(attachment, "", flatten=True)


class FileTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        attachments = message.attachments
        for each in attachments:
            ext = each.filename.split(".")[-1]
            match ext:
                case ".pdf":
                    pdf = True


def setup(bot):
    bot.add_cog(FileTools(bot))
