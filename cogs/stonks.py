# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not have an issue with it.
import disnake
from disnake.ext import commands
from disnake import Option, OptionType
from disnake.ext.commands.errors import CommandInvokeError
import requests
from requests import exceptions

class Stonks(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.cryptolist=requests.get("https://api.coingecko.com/api/v3/coins/list").json()
    
    @commands.slash_command(
        name="stonk",
        description="Get the value of your favorite stonk!",
        options=[
            Option("stonk","The stonk to check!!!", OptionType.string, required=True)
        ]
    )
    async def stonk(self, ctx, stonk):
        stonk="".join([letter for letter in stonk.upper() if letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'])
        if not len(stonk) in [2,3,4]:
            await ctx.response.send_message("Uh oh... I don't think that's a stonk!")
            return
        response=requests.get(f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={stonk}", headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'TE': 'trailers',
        })
        try:
            data=response.json()['quoteResponse']['result'][0]
            price=data['regularMarketPrice']
            name=data['longName']
            change=str(data['regularMarketChangePercent'])
            change=change[:4] if len(change)>4 else change
            await ctx.response.send_message(f"{stonk} ({name}) is currently ${price}, a change of {change}%!")
        except Exception as e:
            await ctx.response.send_message("Oh no! Maybe that isn't a stonk?")
    @commands.slash_command(
        name="crypto",
        description="Get the value of your favorite crypto! Please not a shitcoin!",
        options=[
            Option("crypto","The crypto to check!!!", OptionType.string, required=True)
        ]
    )
    async def crypto(self, ctx, crypto):
        replied=False
        for coin in self.cryptolist:
            if crypto in coin.values():
                try:
                    data=requests.get(f"https://api.coingecko.com/api/v3/coins/{coin['id']}").json()
                    ticker=data['symbol'].upper()
                    name=data['name']
                    price=data['market_data']['current_price']['usd']
                    if not replied:
                        await ctx.response.send_message(f"{ticker} ({name}) is currently ${price}!")
                        replied=True
                    else:
                        await ctx.channel.send(f"{ticker} ({name}) is currently ${price}!")
                except:
                    await ctx.response.send_message("Oh no! Something broke!")
                    replied=True
        if not replied:
            await ctx.response.send_message(f"Couldn't find a crypto for {crypto}")

def setup(bot):
    bot.add_cog(Stonks(bot))