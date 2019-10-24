import discord
from discord.ext import commands
import requests
from helpers import *

class Competitive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def playerInfo(self, player):
        player_url = f"https://www.overbuff.com/players/pc/{'-'.join(player.split('#'))}?mode=competitive"
        url = f"https://ow-api.com/v1/stats/pc/us/{'-'.join(player.split('#'))}/complete"
        data = requests.get(url).json()
        avatar = data['icon']
        sr = data['rating']
        try:
            role_info = {role['role']: (role['level'],[]) for role in data['ratings']}
        except:
            return [player_url,avatar,sr,role_info]
        conv = lambda v: sum([a*b for a,b in zip([1,60,3600], map(int,v[1].split(':')[::-1]))])
        play_time = sorted([[hero, topHeroes['timePlayed']] for hero, topHeroes in data['competitiveStats']['topHeroes'].items()], key=conv)[::-1]
        for hero in play_time:
            if hero[0][:3] in 'anabapbrilucmermoizen':
                role_info["support"][1].append(hero[0])
            elif hero[0][:3] in 'dVaorireiroasigwinwreczar':
                role_info["tank"][1].append(hero[0])
            elif len(role_info["damage"][1])<3: 
                role_info["damage"][1].append(hero[0])
        return [player_url,avatar,sr,role_info]
    
    @commands.command()
    async def sr(self, ctx, player : str):
        player_url, avatar, skill_rating, role_info = await self.playerInfo(player)
        emoji = rankEmoji(skill_rating)
        embed = discord.Embed(title=player, url=player_url, description=f"{emoji}{skill_rating}", inline=False, color=0xff8900)
        embed.set_thumbnail(url=avatar)
        for role in role_info:
            sr = role_info[role][0]
            if(not sr): continue
            e = rankEmoji(sr)
            heroes = role_info[role][1][:3]
            role_emoji = hero_dict[role.lower()]
            hero_emojis = ' '.join(hero_dict[h] for h in heroes)
            embed.add_field(name=f"{role_emoji} {e}{sr}", value= hero_emojis, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Competitive(bot))