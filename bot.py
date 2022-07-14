import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import aiohttp

intnts = discord.Intents.all()
intnts.members = True

load_dotenv()
Token = os.getenv('bot_token')
appid = os.getenv('app_id')

desc = '''Python Message Encryption Bot'''

class CipherBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='$', intents=intnts, application_id=appid)

    async def setup_hook(self):
        await self.load_extension(f"cogs.UtilsAndMiscellaneous")
        await self.load_extension(f"cogs.Cryptography")
        await self.tree.sync()

    async def close(self):
        await super().close()
        await self.session.close()
        
    async def on_ready(self):
        await bot.change_presence(status=discord.Status.online, activity=discord.Game('hard to get'))
        print('Logged in as:')
        print(bot.user.name)
        print(bot.user.id)
        print('----------')

'''
bot = commands.Bot(command_prefix='$', intents=intnts, application_id=996571275919097898)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('hard to get'))
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')

initial_extensions = []
for filename in os.listdir('./cogs'):
    if(filename.endswith('.py')):
       initial_extensions.append("cogs." + filename[:-3])


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    #print('cogs:', initial_extensions)
'''
bot = CipherBot()
bot.run(Token)
