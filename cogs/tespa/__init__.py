import discord
from discord.ext import commands
#from bs4 import BeautifulSoup
#import requests
#from helpers import *
#from multiprocessing import Pool

class Tespa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    '''
    def playerInfo(self, player):
        player_url = f"https://www.overbuff.com/players/pc/{'-'.join(player.split('#'))}?mode=competitive"
        url = f"https://ow-api.com/v1/stats/pc/us/{'-'.join(player.split('#'))}/complete"
        data = requests.get(url).json()
        avatar = data['icon']
        sr = data['rating']
        role_info = {"tank": (0,[]), "damage": (0,[]), "support": (0,[])}
        try:
            for role in data['ratings']:
                role_info[role['role']] = (role['level'],[])
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
    async def zzz(self, ctx, team : str):
        competitive = self.bot.get_cog('Competitive')
        await ctx.send("Fetching team, this might take a while...")
        if "tespa" in team:
            s = BeautifulSoup(requests.get(team).content, 'html.parser')
            teamName = s.find('span', class_="hdg-em").text
            players = [t.next_element.next_element.next_element.text for t in s.find_all('td', class_='compete-player-name')]
            embed = discord.Embed(title=teamName, url=team, description="Overwatch Collegiate Championship: Preseason", color=0xff8040)
            embed.set_thumbnail(url="https://bnetcmsus-a.akamaihd.net/cms/page_media/ZLBKJ6G87QM31492710433537.png")
        else:
            s = requests.get('https://dtmwra1jsgyb0.cloudfront.net/tournaments/5d6fdb02c747ff732da36eb4/teams?name={}'.format(team)).json()
            url = f"https://battlefy.com/teams/{s[0]['persistentTeamID']}"
            players = [p['inGameName'] for p in s[0]['players']]
            embed = discord.Embed(title=team, url=url, description="2019 Overwatch Open Division Practice Season - North America", color=0xff8040)
            embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/3/30/Open_Division_2018_logo.png/540px-Open_Division_2018_logo.png")
        highest_avg = []
        average = []
        #for player in bnet:
            #player_url, avatar, skill_rating, role_info = await competitive.playerInfo(player)
        with Pool(12) as p:
            p_info = p.map(competitive.playerInfo, players)
        print(p_info)
        for i in range(len(p_info)):
            player_url, avatar, skill_rating, role_info = p_info[i]
            player = players[i]
            if skill_rating:
                top_role = [{role: role_info[role]} for role in role_info if role_info[role][0] == max(role[0] for role in role_info.values())][0]
                average.append(skill_rating)
                e = rankEmoji(skill_rating)
                role = list(top_role.keys())[0]
                role_rating = list(top_role.values())[0][0]
                heroes = list(top_role.values())[0][1][:3]
                role_emoji = hero_dict[role.lower()]
                role_rank_emoji = rankEmoji(role_rating)
                hero_emojis = ""
                for hero in heroes:
                    hero_emojis += hero_dict[hero]
                highest_avg.append(role_rating)
            else:
                e = "N/A"
                skill_rating = ""
                role_emoji = "N/A"
                role_rank_emoji = ""
                role_rating = ""
                hero_emojis = ""
            embed.add_field(name = f"{player}: {e}{skill_rating}", value = f"{role_emoji} {role_rank_emoji}{role_rating} {hero_emojis}", inline = False)
        avg = sum(average)//len(average)
        h_avg = sum(highest_avg)//len(highest_avg)
        h_e = rankEmoji(h_avg)
        a_e = rankEmoji(avg)
        embed.add_field(name="Average", value = f"{a_e}{avg}", inline=False)
        embed.add_field(name="Highest Average", value = f"{h_e}{h_avg}", inline=False)
        embed.set_footer(text="N/A = Player profile private or not yet placed.")
        await ctx.send(embed=embed)
    '''

def setup(bot):
    bot.add_cog(Tespa(bot))