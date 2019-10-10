import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print(f'Ready {bot.user}')

for filename in os.listdir('./cogs'):
    bot.load_extension(f'cogs.{filename}')
    print(f'{filename} cog loaded')

try:
    with open('pass.txt') as p:
        secret = p.read()
    bot.run(secret)
except:
    bot.run(os.environ.get('secret_key'))