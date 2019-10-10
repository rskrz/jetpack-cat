import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx):
        import random
        roles = ['Damage','Tank','Support']
        output = random.choice(roles)
        await ctx.send(output)

def setup(bot):
    bot.add_cog(General(bot))