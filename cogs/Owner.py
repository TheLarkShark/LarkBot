import discord
from discord.ext import commands
import random
import math
from random import randint
import datetime
import asyncio
import time
from discord import User
from discord.ext.commands import Bot
from pypubg import core
from time import gmtime

class Owner():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @commands.is_owner()
    async def status(self, ctx):
        'Changes bot status'
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), 'status')
            return
    
    @status.command()
    async def game(self,ctx,*,newstatus:str):
        'Changes bot playing status'
        await self.bot.change_presence(activity=discord.Game(name=newstatus))
    
    @status.command()
    async def streaming(self,ctx,newstatus:str, streamurl:str):
        'Changes bot streaming status. Status must be in quotes'
        await self.bot.change_presence(activity=discord.Streaming(name=newstatus, url=streamurl))
    
    @status.command()
    async def watching(self,ctx,*,newstatus:str):
        'Changes bot watching status'
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=newstatus))
    
    @status.command()
    async def listening(self,ctx,*,newstatus:str):
        'Changes bot listening to status'
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=newstatus))

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        'Shuts down the bot'
        await ctx.send('Off into oblivion!')
        await self.bot.close()
    
    @commands.command()
    @commands.is_owner()
    async def name(self,ctx,*, new_name:str):
        'Changes the bot\'s name'
        await self.bot.user.edit(username=new_name)
        await ctx.send("Name changed")
    
    @commands.command()
    @commands.is_owner()
    async def guilds(self,ctx):
        'Lists all the servers the bot is in'
        guilds = list(self.bot.guilds)
        await ctx.send("I'm in {} servers".format(str(len(self.bot.guilds))))
        for x in range (len(guilds)):
            await ctx.send(" {} - {} - {}".format(guilds[x-1].name,guilds[x-1].id, await self.bot.guilds[x-1].invites()))


def setup(bot):
    bot.add_cog(Owner(bot))
