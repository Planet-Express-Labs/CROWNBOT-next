# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.
import json
from typing import Text
import disnake
import openai
from disnake.ext import commands
import wikipediaapi
import httpx


async def gpt_3_correct(ctx, text: Text):
    """
        Cleans gramatical errors in the text, but using gpt-3.
        :Context ctx:
        """
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Original: {text}\nStandard American English:",
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    await ctx.response.send_message(response.choices[0].text)


def find_confusing(text: str) -> str:
    """
        Finds confusing words in a sentence
        :param text:
        :return:
        """
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"""Find potentially confusing words or brands in the following sentences.
    Sentence: Because Windows NT was designed for the NTen architecture originally
    Confusing: Windows NT, NTen architecture
    Sentence: {text}
    Confusing:""",
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=2,
        presence_penalty=0.0,
        stop=["\n"]
    )
    return response.choices[0].text.split(", ")


class OpenAI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.slash_command(name="explain-code", brief="Explains complicated code using AI")
    # async def cmd_explain_code(self, ctx, code: str = commands.Param()):
    #     """
    #     Explains complicated code using AI
    #     :Context ctx:
    #     :string code:
    #     """
    #     response = openai.Completion.create(
    #         engine="davinci-codex",
    #         prompt=code + "Here's what the above class is doing:\n1.",
    #         temperature=0,
    #         max_tokens=64,
    #         top_p=1.0,
    #         frequency_penalty=0.0,
    #         presence_penalty=0.0,
    #         stop=["\"\"\""]
    #     )
    #     await ctx.response.send_message(response.choices[0].text)

    @commands.slash_command(name="gpt3_correct",
                            brief="Clears gramatical errors in the input text using gpt-3")
    async def cmd_gpt3_correct(self, ctx, text: str = commands.Param()):
        await gpt_3_correct(ctx, text)

    @commands.message_command(name="wikipedia")
    async def ctx_wikipedia(self, ctx: disnake.ApplicationCommandInteraction, message: disnake.Message):
        """
        Automatically finds confusing words and searches them on wikipedia.
        :param ctx: Context
        :param message: Message returned from command
        :return:
        """
        await ctx.response.defer()
        terms = find_confusing(message.content)
        embed = disnake.Embed(title="Located terms", color=0x80bee6)
        for index, each in enumerate(terms):
            embed.add_field(name=str(index + 1), value=each)
        embed.set_footer(text=f"{len(terms)} terms found.")

        menu = disnake.ui.Select(placeholder="Select a term to search for.")
        for index, each in enumerate(terms):
            menu.add_option(
                label=f"{str(index + 1)}. {each}"
            )
        menu_inter = None

        def callback(inter) -> bool:
            callback.inter = inter
            if inter.component.custom_id == menu.custom_id:
                return True
        await ctx.edit_original_message(embed=embed, components=[menu])
        try:
            await ctx.bot.wait_for("dropdown", check=callback)
        except TimeoutError:
            return await ctx.edit_original_message(content="This menu has timed out. Please try again.", embed=None, components=None)
        if callback.inter is None:
            await ctx.edit_original_message(content="Something went wrong... Try again?", embed=None, components=None)
        print(callback.inter.values)
        option = int(callback.inter.values[0][:1])

        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://api.duckduckgo.com/?q={terms[option-1]}&format=json&no_html=1")
        response = response.json()

        if response['Abstract'] == "":
            return await ctx.edit_original_message(content="No results found.", embed=None, components=None)

        # Create an embed using content from DDG API
        embed = disnake.Embed(title=response['Heading'], description=response['AbstractText'], color=0x80bee6)
        if response["Image"] != "":
            embed.set_image(url="https://duckduckgo.com" + response["Image"])
        if response['Definition'] != "" and response["Abstract"] != response["Definition"]:
            embed.add_field(name="definition",
                            value=f"{response['Definition']}\n\n{response['DefinitionSource']}\n"
                                  f"{response['DefinitionURL']}")
        embed.set_footer(text=f"CROWNBOT | Powered by DuckDuckGo",
                         icon_url="https://duckduckgo.com/assets/common/dax-logo.svg")
        embed.set_author(name=response['AbstractSource'])

        await ctx.edit_original_message(embed=embed, components=None)


def setup(bot):
    bot.add_cog(OpenAI(bot))
