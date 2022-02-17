# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.
import re
from typing import List

import disnake
from tortoise import Tortoise


class Menu(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        """
        Discord embed based menu system.
        :param embeds: A list of embeds to be displayed in the menu.
        """
        super().__init__(timeout=None)
        self.embeds = embeds
        self.embed_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.additional_components = []
        self.model_components = []

        # Sets the footer of the embeds with their respective page numbers.
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")
            terms = re.findall(r"%([^;]*)", embed.description)
            # grab the button declarations
            if any(terms):
                embed.description = embed.description.replace(
                    f"%{terms[0]}", "")
                for each in terms:
                    if each[0:7] == "%TOGGLE":
                        params = each.replace(
                            '(', '').replace(')', '').split(', ')
                        models = Tortoise.describe_models()
                        for model in models:
                            name = model.__name__
                            if name.lower == params[0]:
                                self.model_components.append(
                                    (params[3], model))
                                break
                        self.additional_components.append(
                            disnake.ui.Button(
                                label=params[2],
                                custom_id=params[3]
                            )
                        )

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
    async def first_page(self, interaction: disnake.MessageInteraction):
        self.embed_count = 0
        embed = self.embeds[self.embed_count]
        embed.set_footer(text=f"Page 1 of {len(self.embeds)}")

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.next_page.disabled = False
        self.last_page.disabled = False
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="◀")
    async def prev_page(self, interaction: disnake.MessageInteraction):
        self.embed_count -= 1
        embed = self.embeds[self.embed_count]

        self.next_page.disabled = False
        self.last_page.disabled = False
        if self.embed_count == 0:
            self.first_page.disabled = True
            self.prev_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="❌", style=disnake.ButtonStyle.red)
    async def remove(self, interaction: disnake.MessageInteraction):
        await interaction.response.edit_message(view=None)

    @disnake.ui.button(emoji="▶")
    async def next_page(self, interaction: disnake.MessageInteraction):
        self.embed_count += 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        if self.embed_count == len(self.embeds) - 1:
            self.next_page.disabled = True
            self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
    async def last_page(self, interaction: disnake.MessageInteraction):
        self.embed_count = len(self.embeds) - 1
        embed = self.embeds[self.embed_count]

        self.first_page.disabled = False
        self.prev_page.disabled = False
        self.next_page.disabled = True
        self.last_page.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


class ButtonMenu(Menu):
    def __init__(self, embeds: List[disnake.Embed]):
        """
        Discord embed based menu system.
        :param embeds: A list of embeds to be displayed in the menu.
        """
        super().__init__(timeout=None)
        self.embeds = embeds
        self.embed_count = 0

        self.first_page.disabled = True
        self.prev_page.disabled = True
        self.additional_components = []
        self.model_components = []

        # Sets the footer of the embeds with their respective page numbers.
        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Page {i + 1} of {len(self.embeds)}")
            terms = re.findall(r"%([^;]*)", embed.description)
            # grab the button declarations
            if any(terms):
                embed.description = embed.description.replace(
                    f"%{terms[0]}", "")
                for each in terms:
                    if each[0:7] == "%TOGGLE":
                        params = each.replace(
                            '(', '').replace(')', '').split(', ')
                        models = Tortoise.describe_models()
                        for model in models:
                            name = model.__name__
                            if name.lower == params[0]:
                                self.model_components.append(
                                    (params[3], model))
                                break
                        self.additional_components.append(
                            disnake.ui.Button(
                                label=params[2],
                                custom_id=params[3]
                            )
                        )

    async def interaction_check(self, inter: disnake.MessageInteraction):
        for each in self.model_components:
            if each[0] == inter.component.custom_id:
                break


# class MenuEmbed(disnake.Embed):
#     def __init__(self, *,
#                  colour: Union[int, Colour, _EmptyEmbed] = EmptyEmbed,
#                  color: Union[int, Colour, _EmptyEmbed] = EmptyEmbed,
#                  title: MaybeEmpty[Any] = EmptyEmbed,
#                  type: EmbedType = "rich",
#                  url: MaybeEmpty[Any] = EmptyEmbed,
#                  description: MaybeEmpty[Any] = EmptyEmbed,
#                  timestamp: datetime.datetime = None,
#                  ):
#         super().__init__(colour=colour, color=color, title=title, type=type, url=url, description=description,
#                          timestamp=timestamp)


async def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    return f'\r{prefix} |{bar}| {percent}% {suffix}'
