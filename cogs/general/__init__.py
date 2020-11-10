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

    @commands.command()
    async def covid(self, ctx):
        from bs4 import BeautifulSoup
        import requests
        r = requests.get('https://medcom.uiowa.edu/theloop/covid-19-by-the-numbers')
        s = BeautifulSoup(r.content, 'html.parser')
        results = [t.text for t in s.find_all('td')[4::3]]
        output_message = '''**Current COVID-19 adult inpatients**
        {}

        **Current COVID-19 pediatric inpatients (age <18 years old)**
        {}

        **% Positive symptomatic COVID-19 test results**
        {}

        **Number of UI Health Care employees who have tested positive for COVID-19**
        {}

        **Telehealth Influenza-Like-Illness (ILI) screening (telephone & video appointments)**
        {}

        **ILI clinic visits**
        {}

        '''.format(*results)
        embed = discord.Embed(title="University of Iowa COVID-19 data", description=output_message, color=0xff0000)
        embed.set_footer(text="Sourced from UIHC loop")
        await ctx.send(embed=embed)

    @commands.command()
    async def cf(self, ctx):
        from random import choice
        await ctx.send(choice(['Heads', 'Tails']))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        channel = await self.bot.fetch_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)
        user = await self.bot.fetch_user(ctx.user_id)
        emoji = ctx.emoji
        if emoji == '👍':
            room_name = message.title.split(':')[1]
            role = discord.utils.get(guild.roles, name=room_name)
            await user.add_roles(role)
            await ctx.msg.channel.send(embed=response)

    @commands.command()
    async def room(self, ctx, *args):
        chars = 'abcdefghijklmnopqrstuvwxyz-'
        error = discord.Embed(title="Syntax Error", description="Syntax error in command. Please try \".help room\".")
        room_name = args[0]
        room_name = room_name.replace(' ', '-')
        #assert len(set(room_name)-set(chars)) and len(room_name) < 32
        #await bot.create_channel(ctx.message.server, room_name, type=discord.ChannelType.text)
        embed = discord.Embed(title=f"Join temportary room: {room_name}", description=f"React to join the {room_name} room for 24 h.")
        msg = await ctx.send(embed=embed)
        for emoji in ('👍', '👎'):
            await msg.add_reaction(emoji)


def setup(bot):
    bot.add_cog(General(bot))
