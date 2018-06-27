import discord
from discord.ext import commands
import random
import math
import json
from random import randint
import datetime
import asyncio
import time
import logging
from discord import User
from discord.ext.commands import Bot
from pypubg import core
from time import gmtime

logging.basicConfig(level=logging.INFO)

description = 'LarkBot Commands'
startup_extensions = ['Moderation', 'Fun', 'Utility', 'Owner', 'General', 'YouTube', 'ServerManagement', 'Voice', 'Searches','Errors',]
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    while True:
        await bot.change_presence(activity=discord.Game(name="with you, Billy"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my son, Billy"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="my son Billy screaming"))
        await asyncio.sleep(10)

@bot.command(pass_context=True)
@commands.is_owner()
async def load(ctx, extension_name: str):
    'Loads an extension.'
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send('```py\n{}: {}\n```'.format(type(e).__name__, str(e)))
        return
    await ctx.send('{} loaded.'.format(extension_name))


@bot.command(pass_context=True)
@commands.is_owner()
async def unload(ctx,extension_name: str):
    'Unloads an extension.'
    bot.unload_extension(extension_name)
    await ctx.send('{} unloaded.'.format(extension_name))


@bot.command(pass_context=True)
@commands.is_owner()
async def reload(ctx, extension_name: str):
    'Reloads an extension.'
    bot.unload_extension(extension_name)
    bot.load_extension(extension_name)
    await ctx.send('{} reloaded.'.format(extension_name))


@bot.command(pass_context=True)
async def support(ctx):
    'Links to the support server'
    await ctx.send('If you need support, join the official support server at https://discord.gg/AEyzVwg.')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

class DefaultChannels:
    def __init__(self, file):
        self.file = file
        self.lock = asyncio.Lock()

    @property
    def _channels(self):
        try:
            with open(self.file) as fp:
                obj = json.load(fp)
            self._cache = {int(k): v for k, v in obj.items()}
        except FileNotFoundError:
            self._cache = {}
        finally:
            return self._cache

    async def get_channel(self, guild):
        # Get the ID if it was a guild object, else assume it is an integer.
        guild = guild.id if isinstance(guild, discord.Guild) else int(guild)

        return await asyncio.get_event_loop().run_in_executor(None, self._channels.get, guild)

    async def set_channel(self, guild, channel):
        guild = guild.id if isinstance(guild, discord.Guild) else int(guild)
        channel = channel.id if isinstance(channel, discord.TextChannel) else int(channel)

        # Prevents mutation while updating the state on disk, as we await.
        async with self.lock:
            data = self._channels
            data[guild] = channel

            def set_value():
                with open(self.file, 'w') as fp:
                    json.dump(data, fp)

            await asyncio.get_event_loop().run_in_executor(None, set_value)

            # Purge cache
            if '_channels' in self.__dict__:
                del self.__dict__['_channels']

bot.default_channels = DefaultChannels('default_channels.json')

bot.run()
