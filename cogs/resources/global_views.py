import disnake
from disnake.ext import commands


class PersistentView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        print("Creating persistent buttons...")

    @disnake.ui.button(label="Green",
                       style=disnake.ButtonStyle.green,
                       custom_id="persistent_view:green")
    async def green(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("This is green.", ephemeral=True)

    @disnake.ui.button(label="Red",
                       style=disnake.ButtonStyle.red,
                       custom_id="persistent_view:red")
    async def red(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("This is red.", ephemeral=True)

    @disnake.ui.button(label="Grey",
                       style=disnake.ButtonStyle.grey,
                       custom_id="persistent_view:grey")
    async def grey(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("This is grey.", ephemeral=True)
