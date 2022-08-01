import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import button, View, Button
from discord.interactions import Interaction
import json
import requests
import os

opt1 = "Yes"
opt2 = "No"
class Menu(View):
    def __init__(self, timeout=300, op1="Yes", op2="No"):
        super().__init__(timeout=timeout)
        self.opt1count = 0
        self.opt2count = 0
        self.o1 = op1
        self.o2 = op2
        self.voted = []

    @button(label=opt1, style=discord.ButtonStyle.green)
    async def b1(self, interaction:Interaction, button:Button):
        if(interaction.user in self.voted):
            await interaction.response.send_message("You have already voted.", ephemeral=True)
        else:
            self.opt1count += 1
            self.voted.append(interaction.user)
            await interaction.response.send_message(f"You voted {self.o1}", ephemeral=True)
            await interaction.followup.send(f"{self.o1}: {str(self.opt1count)}  |  {self.o2}: {str(self.opt2count)}")

    @button(label=opt2, style=discord.ButtonStyle.blurple)
    async def b2(self, interaction:Interaction, button:Button):
        if(interaction.user in self.voted):
            await interaction.response.send_message("You have already voted.", ephemeral=True)
        else:
            self.opt2count += 1
            self.voted.append(interaction.user)
            await interaction.response.send_message(f"You voted {self.o2}", ephemeral=True)
            await interaction.followup.send(f"{self.o1}: {str(self.opt1count)}  |  {self.o2}: {str(self.opt2count)}")

class Voting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vote(self, ctx, duration: int, opt1: str, opt2: str, *, prompt: str):
        print(ctx.author, 'used vote command')
        v = Menu(duration*60, opt1, opt2)
        v.b1.label = opt1
        v.b2.label = opt2
        opt1 = "yes"
        await ctx.reply(f"Vote: {prompt}", view=v)
    '''
    @commands.command()
    async def vote(self, ctx, minutes: int, option1: str, option2: str, *, prompt: str):
        print(ctx.author, 'used vote command')
        v = Menu(minutes * 60, option1, option2)
        await ctx.reply(f"Vote: {prompt}", view=v)
    '''
async def setup(bot):
    await bot.add_cog(Voting(bot))