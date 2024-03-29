import discord
from discord.ext import commands
from discord.ui import button, View, Button
from discord.interactions import Interaction
from discord import app_commands
import numpy as np
#from Pyfhel import Pyfhel
import os
from dotenv import load_dotenv
import aiohttp

intnts = discord.Intents.all()
intnts.members = True
cryptocurrencykey = os.getenv('cryptocurrencykey')

load_dotenv()
Token = os.getenv('bot_token')
appid = os.getenv('app_id')

desc = '''Python Message Encryption Bot'''

class CipherBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$', help_command = None, intents=intnts, application_id=appid)

    async def setup_hook(self):
        await self.load_extension(f"cogs.UtilsAndMiscellaneous")
        await self.load_extension(f"cogs.Cryptography")
        await self.load_extension(f"cogs.Voting")
        await self.load_extension(f"cogs.Cryptocurrency")
        await self.tree.sync()

    async def close(self):
        await super().close()
        #await self.session.close()
        
    async def on_ready(self):
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('hard to get'))
        print('Logged in as:')
        print(bot.user.name)
        print(bot.user.id)
        print('----------')

bot=CipherBot()

bot.run(Token)
