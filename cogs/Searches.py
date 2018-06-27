import discord
from discord.ext import commands
import random
import math
from random import randint
import datetime
import asyncio
import time
import aiohttp
import re
import urbandictionary as ud
from discord import User
from discord.ext.commands import Bot
from pypubg import core
from time import gmtime


class Searches():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def urban(self, ctx, *, word: str):
        'Searches Urban Dictionary'
        defs = ud.define(word)
        for d in defs:
            embed = discord.Embed(title=word, description=d.definition, color=745822)
            embed.set_footer(text='Urban Dictionary')
            await ctx.send(embed=embed)
    
    @commands.group(no_pm=True)
    async def youtube(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), 'youtube')
    
    @youtube.command(no_pm=True)
    async def search(self,ctx,*,query:str):
        'Search for videos from Youtube'
        try:
            url = 'https://www.youtube.com/results?'
            payload = {'search_query': ''.join(query)}
            headers = {'user-agent': 'Red-cog/1.0'}
            conn = aiohttp.TCPConnector()
            session = aiohttp.ClientSession(connector=conn)
            async with session.get(url, params=payload, headers=headers) as r:
                result = await r.text()
            await session.close()
            yt_find = re.findall(r'href=\"\/watch\?v=(.{11})', result)
            url = 'https://www.youtube.com/watch?v={}'.format(yt_find[0])
            await ctx.send(url)
        except Exception as e:
            message = 'Something went terribly wrong! [{}]'.format(e)
            await ctx.send(message)


def setup(bot):
    bot.add_cog(Searches(bot))