from disnake.ext import commands
import disnake


class BaseModal(disnake.ui.Modal):
    def __init__(self) -> None:
        components = [None]
        super().__init__(title="Create Tag", custom_id="create_tag", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        embed = disnake.Embed(title="Tag Creation")
        for key, value in inter.text_values.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await inter.response.send_message(embed=embed)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        await inter.response.send_message("Something went wrong while processing the modal. "
                                          "Please report this issue to us if it persists.", ephemeral=True)


class FilteringModal(BaseModal):
    def __init__(self) -> None:
        components = [
            disnake.ui.TextInput(name="filter_name", label="Filter Name", placeholder="Enter a name for this filter"),
            disnake.ui.TextInput(name="filter_type", label="Filter Type", placeholder="Enter the type of filter"),
            disnake.ui.TextInput(name="filter_value", label="Filter Value", placeholder="Enter the value of the filter"),
        ]
        super().__init__(components=components)

