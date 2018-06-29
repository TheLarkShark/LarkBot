import discord
from discord.ext import commands
import random
import math
from random import randint
import datetime
import asyncio
import time
import pandas as pd
import openpyxl
import xlsxwriter
from discord import User
from discord.ext.commands import Bot
from pypubg import core
from time import gmtime


class General():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def choose(self, ctx, *choices: str):
        'Chooses between multiple choices.'
        await ctx.send(random.choice(choices))

    @commands.command(pass_context=True)
    async def repeat(self, ctx, times: int, content='repeating...'):
        'Repeats a message multiple times.'
        for i in range(times):
            await ctx.send(content)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        'pseudo-ping time'
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.send(':ping_pong: ({}ms)'.format(round((t2 - t1) * 1000)))

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        'Returns an invite link for the bot'
        await ctx.send('Use this link to invite me to your server\nhttp://bit.ly/LB-Invite')

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        'Flips a coin.'
        choose = ['heads', 'tails']
        flip = random.choice(choose)
        await ctx.send(('The coin landed on ' + flip) + '!')

    @commands.command(pass_context=True,no_pm=True)
    async def poll(self, ctx, question: str, *options: str):
        'Creates a poll. Question MUST be in quotes (i.e. "Is a hot dog a sandwich?")'
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return
        if ((len(options) == 2) and (options[0] == 'yes')) or ((options[0] == 'Yes') and
                                                               (options[1] == 'no')) or (options[1] == 'No'):
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        description = []
        for (x, option) in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description), color=745822)
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        await react_message.edit(embed=embed)
    
    @commands.group()
    async def submit(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), 'submit')
    
    @submit.command()
    async def feedback(self,ctx,*,feedback:str):
        'Sends feedback to the bot owner'
        author=ctx.message.author
        if ctx.message.guild is None:
            source = "DM"
        else:
            source = ctx.message.guild
        channel = self.bot.get_user(197096248413650946)
        embed=discord.Embed(title="Feedback From {}#{} via {}".format(author.name,author.discriminator,source), description=feedback, color=745822)
        embed.set_footer(text="User ID: {}".format(author.id))
        try:
            await channel.send(embed=embed)
        except discord.InvalidArgument:
            await ctx.send("I cannot send your message, I'm unable to find"
                               " my owner... *sigh*")
        except discord.HTTPException:
            await ctx.send("Your message is too long.")
        except:
            await ctx.send("I'm unable to deliver your message. Sorry.")
        else:
            await ctx.send("Your message has been sent.")
    
    @submit.command()
    async def joke(self,ctx,setup:str,punchline:str):
        'Submits a joke for approval'
        me = self.bot.get_user(197096248413650946)
        author = ctx.message.author
        author_id = self.bot.get_user(author.id)
        if ctx.message.guild is None:
            source = "DM"
        else:
            source = ctx.message.guild
        embed=discord.Embed(title="Joke Submission From {}#{} via {}".format(author.name,author.discriminator,source), description="{}\n{}".format(setup,punchline), color=745822)
        embed.set_footer(text="User ID: {}".format(author.id))
        new_joke = await me.send(embed=embed)
        reactions = ['✅', '❌']
        for reaction in reactions:
            await new_joke.add_reaction(reaction)
        
        def check(reaction, me):
            return me and str(reaction.emoji) == '✅'
        try:
            reaction, me = await self.bot.wait_for('reaction_add',check=check)
            df = pd.read_excel("/Users/LarkShark/Downloads/LarkBot/jokes.xlsx",sheetname="Sheet 1 - jokes")
            df2=pd.Series([setup,punchline],index=["Setup","Punchline"])
            df=df.append(df2, ignore_index=True)

            writer = pd.ExcelWriter("/Users/LarkShark/Downloads/LarkBot/jokes.xlsx",engine="xlsxwriter")
            df.to_excel(writer,sheet_name="Sheet 1 - jokes")
            writer.save()

            
            await author_id.send("Your joke has been approved!")
        except asyncio.TimeoutError:
            await ctx.send ('blah')
            


def setup(bot):
    bot.add_cog(General(bot))
