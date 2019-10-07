import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from helpers import *
import asyncio

async def analyzeTeam(self, team):
    competitive = self.bot.get_cog('Competitive')
    if 'tespa' in team:
        s = BeautifulSoup(requests.get(team).content, 'html.parser')
        team = s.find('span', class_="hdg-em").text
        bnet = [t.next_element.next_element.next_element.text for t in s.find_all('td', class_='compete-player-name')]
    else:
        s = requests.get('https://dtmwra1jsgyb0.cloudfront.net/tournaments/5c7ccfe88d004d0345bbd0cd/teams?name={}'.format(team)).json()
        bnet = [p['inGameName'] for p in s[0]['players']]
    outputDict = {}
    average = []
    for player in bnet:
        player_url, avatar, skill_rating, role_info = competitive.playerInfo(player)
        if skill_rating is not 0:
            average.append(skill_rating)
        top_role = [{role: role_info[role]} for role in role_info if role_info[role][0] == max(role[0] for role in role_info.values())][0]
        outputDict[player] = (skill_rating,top_role)
    avg = sum(average)//len(average)
    return outputDict, team, avg

class Tespa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def tespa(self, ctx, team : str):
        team_players, teamName, avg = await analyzeTeam(self, team)
        e = rankEmoji(avg)
        if "tespa" in team:
            embed = discord.Embed(title=teamName, url=team, description="Average: "+str(avg)+e, color=0xff8040)
            embed.set_thumbnail(url="https://bnetcmsus-a.akamaihd.net/cms/page_media/ZLBKJ6G87QM31492710433537.png")
        else:
            embed = discord.Embed(title=teamName, description="SR of team", color=0xff8040)
            embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/3/30/Open_Division_2018_logo.png/540px-Open_Division_2018_logo.png")
        highest_avg = []
        for player in team_players:
            skill_rating = team_players[player][0]
            e = rankEmoji(skill_rating)
            role_info = team_players[player][1]
            role = list(role_info.keys())[0]
            role_rating = list(role_info.values())[0][0]
            heroes = list(role_info.values())[0][1]
            role_emoji = hero_dict[role.lower()]
            role_rank_emoji = rankEmoji(role_rating)
            hero_emojis = ""
            for hero in heroes:
                hero_emojis += hero_dict[hero]
            if role_rating is not 0:
                highest_avg.append(role_rating)
            embed.add_field(name = f"{player}: {e}{skill_rating}", value = f"{role_emoji} {role_rank_emoji}{role_rating} {hero_emojis}", inline = False)
        h_avg = sum(highest_avg)//len(highest_avg)
        h_e = rankEmoji(h_avg)
        embed.add_field(name="Highest Average", value = f"{h_e}{h_avg}", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Tespa(bot))