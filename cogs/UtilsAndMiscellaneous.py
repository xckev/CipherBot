import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
import json
import requests
import os

"""
Fun random stuff and server utilities
"""

class UtilsAndMiscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hello(self, ctx):
        print(ctx.author, 'used hello command')
        await ctx.send('hi!')

    @commands.command()
    async def help(self, ctx):
        print(ctx.author, 'used help command')
        await ctx.send("```Secure Voting \n - $vote <duration> <option 1> <option 2> <prompt> : Creates a 2-option poll with a prompt that accepts submissions for a specified number of minutes. Use quotation marks to separate arguments that have spaces. \n \nCryptography \n - $keygen :  Generates new Diffie-Hellman private and public keys for encryption and decryption. Execute often for better security. /encrypt calls this automatically if keys were not previously generated. \n - /encrypt :  Encrypt a secret message to send to a user of choice \n - /decrypt :  Decrypts ciphertext that was sent by someone \n\nCryptocurrency \n - $crypto <coin symbol> : Shows the price of the requested coin \n - $bitcoin : Shows the price of BTC \n - $ethereum : Shows the price of ETC \n - $dogecoin : Shows the price of DOGE \n\nUtilities and Miscellaneous \n - $help :  CipherBot information and commands \n - $hello :  Exchange greetings with Cipherbot! \n - $kick :  Mention a user to kick from the server \n - $ban :  Mention a user to ban from the server \n - $shutdown :  CipherBot will go offline; only the bot's host may use this \n```")

    @commands.Cog.listener()
    async def on_message(self, message):
        if(message.content == "bad bot"):
            await message.channel.send(":'(")
        elif(message.content == "good bot"):
            await message.channel.send(":)")
        elif(message.content == "POG"):
            await message.channel.send("CHAMP")
        elif(message.content.lower() == "pog"):
            await message.channel.send("champ")

        #await self.bot.process_commands(message)

    @commands.command()
    @has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        print(ctx.author, 'used kick command')
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked')
        
    @kick.error
    async def kick_error(self, ctx, error):
        print('kick error')
        if(isinstance(error, MissingPermissions)):
            await ctx.send("You don't have permission to kick people!")
        else:
            await ctx.send("Couldn't kick that user.")

    @commands.command()
    @has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        print(ctx.author, 'used ban command')
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned')
        
    @ban.error
    async def ban_error(self, ctx, error):
        print('ban error')
        if(isinstance(error, MissingPermissions)):
            await ctx.send("You don't have permission to ban people!")
        else:
            await ctx.send("Couldn't ban that user.")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("CipherBot is now offline. All keys must be regenerated once CipherBot is online again.")
        exit()
        
async def setup(bot):
    await bot.add_cog(UtilsAndMiscellaneous(bot))
