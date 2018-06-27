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
from xlrd import open_workbook
from discord import User
from discord.ext.commands import Bot
from pypubg import core
from time import gmtime


class Fun():
    def __init__(self, bot):
        self.bot = bot
    
    def check_if_it_is_me(self,ctx):
        return ctx.message.author.id == 197096248413650946

    @commands.command(pass_context=True)
    async def roll(self, ctx, dice: str):
        'Rolls a dice in NdN format.'
        try:
            (rolls, limit) = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        result = ', '.join((str(random.randint(1, limit)) for r in range(rolls)))
        await ctx.send(result)

    @commands.group(pass_context=True)
    async def cool(self, ctx):
        'Says if a user is cool.'
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

    @cool.command(pass_context=True,name='bot')
    async def _bot(self, ctx):
        'Is the bot cool?'
        await ctx.send('Yes, the bot is cool.')

    @commands.command(pass_context=True)
    async def rps(self, ctx, choice):
        'Play a game of rock, paper, scissors!'
        t = ['Rock', 'Paper', 'Scissors']  #List of play options
        computer = t[randint(0, 2)]
        choice = choice[0].upper() + choice[1:len(choice)]  #Assign a random play to the computer
        if choice == computer:
            await ctx.send("It's a tie!")
        elif (choice == 'Rock') and (computer == 'Scissors'):
            await ctx.send('You win! Rock smashes ' + computer)
        elif (choice == 'Rock') and (computer == 'Paper'):
            await ctx.send(('You lose! ' + computer) + ' covers Rock')
        elif (choice == 'Paper') and (computer == 'Rock'):
            await ctx.send('You win! Paper covers ' + computer)
        elif (choice == 'Paper') and (computer == 'Scissors'):
            await ctx.send(('You lose! ' + computer) + ' cuts Paper')
        elif (choice == 'Scissors') and (computer == 'Rock'):
            await ctx.send(('You lose! ' + computer) + ' smashes Scissors')
        elif (choice == 'Scissors') and (computer == 'Paper'):
            await ctx.send('You win! Scissors cuts ' + computer)
        else:
            await ctx.send("That's not a valid play. Check your spelling!")

    @commands.command(pass_context=True,no_pm=True)
    async def ship(self, ctx, user1: discord.User, user2: discord.User):
        'Ships 2 users'
        s = user1.name
        l = len(s)
        h = random.randint(0, l)
        z = user2.name
        g = len(z)
        p = random.randint(0, g)
        x = s[:h]
        y = z[p:]
        await ctx.send(x + y)

    @commands.group(pass_context=True)
    async def joke(self, ctx):
        'Tells a joke'
        if ctx.invoked_subcommand is None:
            wb = open_workbook('/Users/LarkShark/Downloads/LarkBot/jokes.xlsx')
            for sheet in wb.sheets():
                numbrows = sheet.nrows
                row = random.randint(1, numbrows - 1)
                setup = sheet.cell(row, 2).value
                punchline = sheet.cell(row, 3).value
            await ctx.send(setup)
            await asyncio.sleep(2)
            await ctx.trigger_typing()
            await asyncio.sleep(2)
            await ctx.send(punchline)
            return
    
    @joke.command()
    @commands.is_owner()
    async def add(self,ctx,setup:str,punchline:str):
        'Adds a new joke'
        df = pd.read_excel("/Users/LarkShark/Downloads/LarkBot/jokes.xlsx",sheetname="Sheet 1 - jokes")
        df2=pd.Series([setup,punchline],index=["Setup","Punchline"])
        df=df.append(df2, ignore_index=True)

        writer = pd.ExcelWriter("/Users/LarkShark/Downloads/LarkBot/jokes.xlsx",engine="xlsxwriter")
        df.to_excel(writer,sheet_name="Sheet 1 - jokes")
        writer.save()

        await ctx.send("Joke added")

    @commands.command(pass_context=True,aliases=['insult'])
    async def roast(self, ctx, user: discord.Member = None):
        'Roasts a user'
        if user is not None:
            with open('/Users/LarkShark/Downloads/LarkBot/Insults.txt') as f:
                lines = f.readlines()
                insult_list = list(lines)
            i = random.randint(1, len(insult_list) - 1)
            await ctx.send((user.mention + ', ') + insult_list[i])
        if user is None:
            await ctx.invoke(self.bot.get_command('help'), 'roast')


def setup(bot):
    bot.add_cog(Fun(bot))