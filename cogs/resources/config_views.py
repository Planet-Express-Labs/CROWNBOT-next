from typing import List
from disnake.ext import commands
import disnake

from database import databases
from utils import paginate
from tortoise.models import Model

# class ImageFilteringView(paginate.Menu):
#     def __init__(self, bot, embeds: List[disnake.Embed]):
#         super().__init__(bot, embeds = embeds)


def to_style(convert) -> disnake.ButtonStyle:
    if isinstance(convert, bool):
        if convert:
            return disnake.ButtonStyle.green
        else:
            return disnake.ButtonStyle.red
    elif isinstance(convert, str):
        if len(convert) == 0:
            return disnake.ButtonStyle.red
        else:
            return disnake.ButtonStyle.green
    elif convert is None:
        return disnake.ButtonStyle.blurple


# TODO: Make this into something that is more extensible.
class ImageFilteringView(disnake.ui.View):
    def __init__(self, db: databases.Server):
        self.db = db
        super().__init__()

    @disnake.ui.button(label="filter NSFW content")
    async def filter_nsfw(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        button.style = to_style(self.db.image_filtering)
        self.db.nsfw = not self.db.nsfw
        await self.db.save()
        button.style = to_style(self.db.image_filtering)

    @disnake.ui.button(label="filter explicit content")
    async def filter_explicit(self, button: disnake.ui.Button, ctx: disnake.MessageInteraction):
        button.style = to_style(self.db.image_filtering)
        self.db.explicit = not self.db.explicit
        await ctx.send(f"Explicit filter set to {to_style(self.db.explicit)}")

    @disnake.ui.button(label="Confirm", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("Saving settings...", ephemeral=True)
        await self.db.save()
        await interaction.response.edit_message("Settings saved!", delete_after=5, ephemeral=True)
        self.stop()

    # This one is similar to the confirmation button except sets the inner
    # value to `False`
    @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.grey)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("Cancelled.", delete_after=5, ephemeral=True)
        self.stop()
