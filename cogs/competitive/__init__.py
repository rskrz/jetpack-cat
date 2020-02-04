import discord
from discord.ext import commands
from helpers import *

class Competitive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def player_info(self, player):
        import requests
        player_url = f"https://www.overbuff.com/players/pc/{'-'.join(player.split('#'))}?mode=competitive"
        url = f"https://ow-api.com/v1/stats/pc/us/{'-'.join(player.split('#'))}/complete"
        data = requests.get(url).json()
        role_info = {"tank": (0,[]), "damage": (0,[]), "support": (0,[])}
        try: sr = data['rating']
        except: sr = 0
        try: avatar = data['icon']
        except: avatar = "avatar"
        try: 
            role_info = {role['role']: (role['level'],[]) for role in data['ratings']}
            roles = ['tank','damage','support']
            for r in roles:
                if r not in role_info.keys(): role_info[r] = (0,[])
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

    async def scrape(self, player):
        from bs4 import BeautifulSoup
        import requests
        player_url = f"https://www.overbuff.com/players/pc/{'-'.join(player.split('#'))}?mode=competitive"
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        s = BeautifulSoup(requests.get(player_url, headers=headers).content, 'html.parser')
        td_list = s.find_all('td')
        if(not td_list):
            player_url = f"https://www.overbuff.com/players/pc/{'-'.join(player.split('#'))}"
            s = BeautifulSoup(requests.get(player_url, headers=headers).content, 'html.parser')
            td_list = s.find_all('td')
        if(not td_list):
            return await self.player_info(player)
        role_info = {"tank": [0,[]], "damage": [0,[]], "support": [0,[]]}
        for td in td_list:
            if td.has_attr("data-value"):
                role = td.previous_sibling.text
                role_sr = td.text.replace(',','')
                if(role=="Damage"):
                    role_info["damage"][0] = int(role_sr)
                elif(role=="Support"):
                    role_info["support"][0] = int(role_sr)
                elif(role=="Tank"):
                    role_info["tank"][0] = int(role_sr)
        try:
            sr = int(s.find("span",attrs={"class":"player-skill-rating"}).text)
        except: sr = 0
        avatar = s.find("img",attrs={"class":"image-player image-avatar"})['src']
        heroes = s.find_all("div",attrs={"class":"name"})
        for hero in heroes:
            name = hero.a.text.lower()
            if name[:3] in 'anabapbrilucmermoizen':
                role_info["support"][1].append(name)
            elif name[:3] in 'dVaorireiroasigwinwreczar':
                role_info["tank"][1].append(name)
            elif len(role_info["damage"][1])<3: 
                role_info["damage"][1].append(name)
        return [player_url,avatar,sr,role_info]
    
    @commands.command()
    async def sr(self, ctx, player : str):
        try:
            player_url, avatar, skill_rating, role_info = await self.scrape(player)
        except:
            return await ctx.send("Player not found.")
        emoji = rankEmoji(skill_rating)
        embed = discord.Embed(title=player, url=player_url, description=f"{emoji}{skill_rating}", inline=False, color=0xff8900)
        embed.set_thumbnail(url=avatar)
        for role in role_info:
            sr = role_info[role][0]
            if(not sr): continue
            e = rankEmoji(sr)
            heroes = role_info[role][1][:3]
            if(heroes):
                hero_emojis = ' '.join(hero_dict[h] for h in heroes)
            else:
                hero_emojis = "N/A"
            role_emoji = hero_dict[role.lower()]
            embed.add_field(name=f"{role_emoji} {e}{sr}", value= hero_emojis, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Competitive(bot))