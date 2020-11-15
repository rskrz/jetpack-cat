import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.rooms = []

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
    """
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            if r:= next((room for room in self.rooms if payload.message_id==room.room_id),None):
                channel = self.bot.get_channel(payload.channel_id)
                msg = discord.utils.get(await channel.history(limit=100).flatten(), channel=channel)
                title = msg.embeds[0].title
                desc = msg.embeds[0].description
                desc += f"\n {payload.member}"
                embed = discord.Embed(title=title, description=desc)
                guild_id = payload.guild_id
                guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
                role = discord.utils.get(guild.roles, name=r.room_name)
                await msg.edit(embed=embed)
                await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id != self.bot.user.id:
            if r:= next((room for room in self.rooms if payload.message_id==room.room_id),None):
                channel = self.bot.get_channel(payload.channel_id)
                msg = discord.utils.get(await channel.history(limit=100).flatten(), channel=channel)
                title = msg.embeds[0].title
                desc = msg.embeds[0].description
                guild_id = payload.guild_id
                guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
                member = await guild.fetch_member(payload.user_id)
                user_str = str(self.bot.get_user(member.id))
                if user_str in desc:
                    desc = desc.replace(user_str,"")
                    embed = discord.Embed(title=title, description=desc)
                    role = discord.utils.get(guild.roles, name=r.room_name)
                    await msg.edit(embed=embed)
                    await member.remove_roles(role)

    @commands.command()
    async def room(self, ctx, *args):
        room_name = "Room: "+" ".join(args)
        guild = ctx.message.guild
        if not any(role.name == room_name for role in guild.roles):
            embed = discord.Embed(title=room_name, description="React with 👍 to join and remove reaction to leave.")
            room_msg = await ctx.send(embed=embed)
            r = Room(room_msg.id,room_name)
            self.rooms.append(r)
            await room_msg.add_reaction('👍')
            await guild.create_role(name=room_name)
        else:
            await ctx.send("That room already exists.")

class Room:
    room_id = 0
    room_name = ""

    def __init__(self, room_id, room_name):
        self.room_id = room_id
        self.room_name = room_name
    """
def setup(bot):
    bot.add_cog(General(bot))
