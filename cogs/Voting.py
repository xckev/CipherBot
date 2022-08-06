import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import button, View, Button
from discord.interactions import Interaction
from Pyfhel import Pyfhel
import numpy as np
import json
import requests
import os

HE = Pyfhel()

def enc(votes):
    HE.contextGen(scheme='bfv', n=2**14, t_bits=20)
    HE.keyGen()

    encvotes = []
    for elem in votes:
        i = np.array([elem], dtype=np.int64)
        ctxt = HE.encryptInt(i)
        encvotes.append(ctxt)
    
    return encvotes

def combine(encvotes):
    ctxtSum = encvotes[0]
    for i in range(1, len(encvotes)):
        ctxtSum += encvotes[i]
    return HE.decryptInt(ctxtSum)

def mix(votes):
    sz = len(votes)
    perm = np.random.permutation(sz)
    m = []
    for elem in perm:
        m.append(votes[elem])
    return m

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
        self.votes = []

    #This commented out code is the voting buttons with mix net emulation and homomorphic encryption.
    #However, the algorithms take too long, and it times out the Discord interaction.
    '''
    @button(label=opt1, style=discord.ButtonStyle.green)
    async def b1(self, interaction:Interaction, button:Button):
        if(interaction.user in self.voted):
            await interaction.response.send_message("You have already voted.", ephemeral=True)
        else:
            self.opt1count += 1
            self.votes.append(1)
            self.voted.append(interaction.user)
            enced = enc(self.votes)
            mixed = mix(enced)
            res = combine(mixed)
            await interaction.response.send_message(f"You voted {self.o1}", ephemeral=True)
            if(res > 0):
                await interaction.followup.send(f"{self.o1} is winning by {res} votes")
            elif(res < 0):
                await interaction.followup.send(f"{self.o2} is winning by {-1 * res} votes")
            else:
                await interaction.followup.send(f"Vote is tied")
            #await interaction.followup.send(f"{self.o1}: {str(self.opt1count)}  |  {self.o2}: {str(self.opt2count)}")

    @button(label=opt2, style=discord.ButtonStyle.blurple)
    async def b2(self, interaction:Interaction, button:Button):
        if(interaction.user in self.voted):
            await interaction.response.send_message("You have already voted.", ephemeral=True)
        else:
            self.opt2count += 1
            self.votes.append(-1)
            self.voted.append(interaction.user)
            enced = enc(self.votes)
            mixed = mix(enced)
            res = combine(mixed)
            await interaction.response.send_message(f"You voted {self.o2}", ephemeral=True)
            if(res > 0):
                await interaction.followup.send(f"{self.o1} is winning by {res} votes")
            elif(res < 0):
                await interaction.followup.send(f"{self.o2} is winning by {-1 * res} votes")
            else:
                await interaction.followup.send(f"Vote is tied")            
            #await interaction.followup.send(f"{self.o1}: {str(self.opt1count)}  |  {self.o2}: {str(self.opt2count)}")
    '''
    @button(label=opt1, style=discord.ButtonStyle.green)
    async def b1(self, interaction:Interaction, button:Button):
        if(interaction.user in self.voted):
            await interaction.response.send_message("You have already voted.", ephemeral=True)
        else:
            self.opt1count += 1
            self.votes.append(1)
            self.voted.append(interaction.user)
            #enced = enc(self.votes)
            #mixed = mix(enced)
            #res = combine(mixed)
            await interaction.response.send_message(f"You voted {self.o1}", ephemeral=True)
            await interaction.followup.send(f"{self.o1}: {str(self.opt1count)}  |  {self.o2}: {str(self.opt2count)}")

    @button(label=opt2, style=discord.ButtonStyle.blurple)
    async def b2(self, interaction:Interaction, button:Button):
        if(interaction.user in self.voted):
            await interaction.response.send_message("You have already voted.", ephemeral=True)
        else:
            self.opt2count += 1
            self.votes.append(-1)
            self.voted.append(interaction.user)
            #enced = enc(self.votes)
            #mixed = mix(enced)
            #res = combine(mixed)
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