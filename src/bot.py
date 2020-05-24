import os

import discord
from dotenv import load_dotenv

from discord.ext import commands
import sys, traceback

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


initial_extensions = ['cogs.fun','cogs.osrs','cogs.ac']

bot = commands.Bot(command_prefix="!")

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Game(name='The Shed', type=1, url='https://twitch.tv/PlizRS'))


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the {GUILD} Discord server! Please be sure to read the rules in the #welcome channel.'
    )


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


bot.run(TOKEN, bot=True, reconnect=True)
