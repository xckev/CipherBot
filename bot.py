import discord
from discord.ext import commands
from discord.ui import button, View, Button
from discord.interactions import Interaction
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
        super().__init__(command_prefix='$', help_command = None, intents=intnts, application_id=appid)

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

bot = CipherBot()

class Menu(View):
    def __init__(self, *, timeout=300):
        super().__init__(timeout=timeout)
        self.yescount = 0
        self.nocount = 0
        self.voted = []
        #self.value = None

    @button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction:Interaction, button:Button):
        if(interaction.user in self.voted):
            await interaction.response.send_message("You have already voted.", ephemeral=True)
        else:
            self.yescount += 1
            self.voted.append(interaction.user)
            await interaction.response.send_message("You voted yes", ephemeral=True)
            await interaction.followup.send(f"Yes: {str(self.yescount)}  |  No: {str(self.nocount)}")
        #await interaction.response.send_message(f"Yes: {str(self.yescount)}  |  No: {str(self.nocount)}")

    @button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction:Interaction, button:Button):
        if(interaction.user in self.voted):
            await interaction.response.send_message("You have already voted.", ephemeral=True)
        else:
            self.nocount += 1
            self.voted.append(interaction.user)
            await interaction.response.send_message("You voted no", ephemeral=True)
            await interaction.followup.send(f"Yes: {str(self.yescount)}  |  No: {str(self.nocount)}")
        #await interaction.response.send_message(f"Yes: {str(self.yescount)}  |  No: {str(self.nocount)}")

@bot.command()
async def vote(ctx, *, question: str):
    v = Menu()
    await ctx.reply(f"Vote: {question}", view=v)


bot.run(Token)
