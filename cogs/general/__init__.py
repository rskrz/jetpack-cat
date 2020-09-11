import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx):
        import random
        roles = ['Damage','Tank','Support']
        await ctx.send(random.choice(roles))

    @commands.command(aliases=['comp', 'heroes'])    
    async def hero(self, ctx, num=1):
        from helpers import heroes_only
        import random
        if num > (max_heroes := len(heroes_only)):
            return await ctx.send(f'Too many heroes! Max {max_heroes}')
        num_list = random.sample(range(0,max_heroes), num)
        heroes = list(heroes_only.keys())
        output = "".join([heroes_only.get(heroes[num]) for num in num_list])
        await ctx.send(output)

    @commands.command()    
    async def roleq(self, ctx):
        from helpers import dps_heroes, tank_heroes, support_heroes
        import random
        heroes = [tank_heroes,dps_heroes,support_heroes]
        emojis = [random.sample(list(i.values()),2)[0:2] for i in heroes]
        output = "".join(["".join(e) for e in emojis])
        await ctx.send(output)

def setup(bot):
    bot.add_cog(General(bot))