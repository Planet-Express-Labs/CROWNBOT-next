# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.
import disnake
from disnake.ext import commands
from disnake import Option, OptionType
from utils.languagetool_utils import get_matches, correct
import requests
from async_google_trans_new import AsyncTranslator
from async_google_trans_new.constant import LANGUAGES
import pycountry


class Language_Dropdown(disnake.ui.Select):
    def __init__(self, languages, text):
        options = [
            disnake.SelectOption(
                label=language[0],
                description=language[1]) for language in languages]
        self.text = text
        super().__init__(
            placeholder='Choose your language!',
            min_values=1,
            max_values=1,
            options=options)

    async def callback(self, interaction):
        lang = self.values[0]
        translator = AsyncTranslator()
        translated = await translator.translate(self.text, lang)
        embed = disnake.Embed(title="Translation")
        embed.add_field(name="Original", value=f"{self.text}")
        embed.add_field(name=f"Translated ({lang})", value=f"{translated}")
        # print(interaction.target)
        await interaction.message.edit(None, embed=embed, view=None)


class Text_Processor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ltool_codes = ['auto'] + [lang['longCode'].lower() for lang in
                                       requests.get("https://api.languagetoolplus.com/v2/languages").json()]
        self.translate_langs = LANGUAGES
        self.translator = AsyncTranslator()

    @commands.slash_command(name="proofread",
                            description="Proofreads and replies with changed text.",
                            options=[Option("text",
                                            "The text to proofread",
                                            OptionType.string,
                                            required=True),
                                     Option("target",
                                            "Language to proofread in (default: en-US)",
                                            OptionType.string)])
    async def cmd_proofread(self, ctx, text, target="auto"):
        prefix = ''
        if target != "auto":
            langs = pycountry.languages
            target = langs.lookup(target).alpha_2
            if target not in self.ltool_codes:
                prefix = f"It seems that your selected language ({target}) is not supported. Language codes should be" \
                         f" formatted by locale (eg. en-US or fr). Falling back to Automatic.\n\n "
                target = "auto"
        matches = await get_matches(text, target)
        if len(matches) == 0:
            await ctx.response.send_message(prefix + "No problems were detected with your text!")
            return
        corrected = correct(text, matches)
        await ctx.response.send_message(prefix + corrected)

    @commands.slash_command(name="translate",
                            description="Translates text to a new language!",
                            options=[Option("text",
                                            "The text to translate",
                                            OptionType.string,
                                            required=True),
                                     Option("target",
                                            "Language to transate to (default: en)",
                                            OptionType.string)])
    async def cmd_translate(self, ctx, text, target="en"):
        prefix = ''
        if target != "en":
            target = target.lower()
            langs = pycountry.languages
            target = langs.lookup(target).alpha_2
            if target not in self.translate_langs:
                prefix = f"It seems your selected language ({target}) is not supported. Language codes should be " \
                         f"formatted by 2-letter locale (eg. en or fr). Falling back to English.\n\n "
                target = "en"
        text = await self.translator.translate(text, target)
        await ctx.response.send_message(prefix + text)

    @commands.message_command(name="proofread")
    async def ctx_proofread(self, ctx):
        text = ctx.target.content
        if not text:
            return
        matches = await get_matches(text, "en")
        if len(matches) == 0:
            await ctx.response.send_message("No problems were detected with your text!")
            return
        corrected = correct(text, matches)
        await ctx.response.send_message(corrected)

    @commands.message_command(name="translate")
    async def ctx_translate(self, ctx):
        text = ctx.target.content
        if not text:
            return
        translated = await self.translator.translate(text, "en")
        await ctx.response.send_message(translated)

    @commands.message_command(name="translate-to")
    async def ctx_translate_to(self, ctx):
        view = disnake.ui.View()
        view.add_item(Language_Dropdown([
            ('zh-cn', 'Chinese (Simplified)'),
            ('zh-tw', 'Chinese (Traditional)'),
            ('es', 'Spanish'),
            ('en', 'English'),
            ('hi', 'Hindi'),
            ('bn', 'Bengali'),
            ('pt', 'Portuguese'),
            ('ru', 'Russian'),
            ('ja', 'Japanese'),
            ('tr', 'Turkish'),
            ('ko', 'Korean'),
            ('fr', 'French'),
            ('de', 'German'),
            ('vi', 'Vietnamese'),
            ('ar', 'Arabic'),
            ('id', 'Indonesian')
        ], text=ctx.target.content))
        await ctx.response.send_message("Pick a language!", view=view)


def setup(bot):
    bot.add_cog(Text_Processor(bot))
