import discord
from discord.ext import commands
from discord import Member
from Test import cryptocurrencykey
import json
import requests
import os

class Cryptocurrency(commands.Cog):

    headers = {
        'X-CMC_PRO_API_KEY' : cryptocurrencykey,
        'Accepts' : 'application/json'
    }
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    json = requests.get(url, headers=headers).json()
    cryto = json['data']

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crypto(self, ctx, symbol):
        for x in self.cryto:
            if x['symbol'] == symbol:
                coin = f"{x['symbol']} Price: ${x['quote']['USD']['price']}"
                await ctx.send(coin)

    @commands.command()
    async def bitcoin(self, ctx):
        for x in self.cryto:
            if x['symbol'] == 'BTC':
                coin = f"{x['symbol']} Price: ${x['quote']['USD']['price']}"
                await ctx.send(coin)

    @commands.command()
    async def ethereum(self, ctx):
        for x in self.cryto:
            if x['symbol'] == 'ETH':
                coin = f"{x['symbol']} Price: ${x['quote']['USD']['price']}"
                await ctx.send(coin)

    @commands.command()
    async def dogecoin(self, ctx):
        for x in self.cryto:
            if x['symbol'] == 'DOGE':
                coin = f"{x['symbol']} Price: ${x['quote']['USD']['price']}"
                await ctx.send(coin)


async def setup(bot):
    await bot.add_cog(Cryptocurrency(bot))