import discord
from discord.ext import commands
from helpers import teams

class Owl(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def owl_schedule(self, week : int):
        import requests
        from datetime import datetime
        from pytz import timezone
        url = "https://api.overwatchleague.com/schedule?expand=team.content&locale=en_US&season=2019"
        data = requests.get(url).json()
        games = []
        stage = 4
        matches = data['data']['stages'][stage]['weeks'][week]['matches']
        for game in matches:
            info = []
            score = {}
            index = 0
            for competitor in game['competitors']:
                score[competitor['abbreviatedName']] = game['scores'][index]['value']
                index += 1
            info.append(score)
            date = datetime.fromtimestamp(game['startDateTS']/1000.0).astimezone(timezone('US/Central')).strftime('%a %b %d %I:%M %p')
            info.append(date)
            games.append(info)
        return(games)

    async def get_schedule(self, week):
        #week = week - 1
        match_info = await self.owl_schedule(week)
        embed = discord.Embed(title="Stage 4 Schedule", url = "https://overwatchleague.com/en-us/schedule", description="Week "+str(week+1), color=0xff8900)
        embed.set_thumbnail(url="https://www.plusforward.net/files/2016/15919/1_ow-league.png")
        for match in match_info:
            team1 = next(value for key, value in teams.items() if list(match[0].keys())[0] in key)
            team2 = next(value for key, value in teams.items() if list(match[0].keys())[1] in key)
            title = f"{team1[3]} {list(match[0].values())[0]} - {list(match[0].values())[1]} {team2[3]}"
            desc = match[1]
            embed.add_field(name=title, value=desc, inline=True)
        return embed

    @commands.command(desc="schedule", aliases=['sc'])
    async def schedule(self, ctx):
        embed = await self.get_schedule(0)
        msg = await ctx.send(embed=embed)
        emojis = ["\u0031\u20E3","\u0032\u20E3","\u0033\u20E3","\u0034\u20E3","\u0035\u20E3"]
        for emoji in emojis:
            await msg.add_reaction(emoji)
        @commands.Cog.listener()
        async def on_reaction_add(self,reaction, user):
            print('yo')
            if reaction.message.id == msg.id and user != self.bot.user:
                if reaction.emoji in emojis:
                    new = await self.get_schedule(emojis.index(reaction.emoji))
                await msg.edit(embed=new)
                await msg.remove_reaction(reaction.emoji,user)

def setup(bot):
    bot.add_cog(Owl(bot))