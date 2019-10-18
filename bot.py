import discord
import os
from discord.ext import commands
from helpers import *

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'Ready {bot.user}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('jetpackcat.tech'))

def owl_schedule(week : int):
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

def get_schedule(week):
    #week = week - 1
    match_info = owl_schedule(week)
    embed = discord.Embed(title="Stage 4 Schedule", url = "https://overwatchleague.com/en-us/schedule", description="Week "+str(week+1), color=0xff8900)
    embed.set_thumbnail(url="https://www.plusforward.net/files/2016/15919/1_ow-league.png")
    for match in match_info:
        team1 = next(value for key, value in teams.items() if list(match[0].keys())[0] in key)
        team2 = next(value for key, value in teams.items() if list(match[0].keys())[1] in key)
        title = f"{team1[3]} {list(match[0].values())[0]} - {list(match[0].values())[1]} {team2[3]}"
        desc = match[1]
        embed.add_field(name=title, value=desc, inline=True)
    return embed

@bot.command(desc="schedule", aliases=['sc'])
async def schedule(ctx):
    embed = get_schedule(0)
    msg = await ctx.send(embed=embed)
    emojis = ["\u0031\u20E3","\u0032\u20E3","\u0033\u20E3","\u0034\u20E3","\u0035\u20E3"]
    for emoji in emojis:
        await msg.add_reaction(emoji)
    @bot.event
    async def on_reaction_add(reaction, user):
        if reaction.message.id == msg.id and user != bot.user:
            if reaction.emoji in emojis:
                new = get_schedule(emojis.index(reaction.emoji))
            await msg.edit(embed=new)
            await msg.remove_reaction(reaction.emoji,user)

def owl_standings(standingsType):
    import requests
    url = "https://api.overwatchleague.com/v2/standings?locale=en_US&season=2019"
    data = requests.get(url).json()
    scores = [None]*20
    for team in data['data']:
        score = []
        if standingsType == 'playoffs':
            try:
                stage = team['divLeader']
            except: 
                stage = team['wildcard']
        else:
            stage = team['stages'][standingsType]
        placement = stage['placement']
        matchWin = stage['matchWin']
        matchLoss = stage['matchLoss']
        differential = str(stage['comparisons'][2]['value'])
        if stage['comparisons'][1]['value'] > 0:
            differential = f"+{differential}"
        score.append(team['abbreviatedName'])
        score.append(matchWin)
        score.append(matchLoss)
        score.append(differential)
        extraSpots = 0
        if scores[placement-1] is not None:
            extraSpots += 1
        if scores[placement-1+extraSpots] is None:
            scores[placement-1+extraSpots] = score
        else:
            scores[placement+extraSpots] = score
    return scores

def get_standings(standingsType):
    teamStandings = owl_standings(standingsType)
    if standingsType == 'stage1':
        desc = "Stage 1"
    elif standingsType == 'stage2':
        desc = "Stage 2"
    elif standingsType == 'stage3':
        desc = "Stage 3"
    elif standingsType == 'stage4':
        desc = "Stage 4"
    else:
        desc = "Playoffs"
    embed = discord.Embed(title="OWL Standings",description=desc,url="https://overwatchleague.com/en-us/standings/season/2019/stage/3",color=0xff8040)
    embed.set_thumbnail(url="https://www.plusforward.net/files/2016/15919/1_ow-league.png")
    embed.set_footer(text="1-4 = Stage #, P = Playoffs")
    new = [None]*20
    for t in teamStandings:
        i = teamStandings.index(t)
        if i < 10:
            new[2*i] = t
        else:
            new[2*i-19] = t
    for teamInfo in new:
        teamName, teamWins, teamLosses, teamDiff = teamInfo[0], teamInfo[1], teamInfo[2], teamInfo[3]
        teamEmoji = next(value for key, value in teams.items() if teamName in key)[3]
        rank = teamStandings.index(teamInfo) + 1
        name = f'{rank}. {teamEmoji}  {teamWins} - {teamLosses}'
        value = f'DIFF: {teamDiff}'
        embed.add_field(name=name, value=value, inline=True)
    return embed

@bot.command(desc='standings',aliases=['st'])
async def standings(ctx):
    embed = get_standings('stage4')
    msg = await ctx.send(embed=embed)
    emojis = ["\u0031\u20E3","\u0032\u20E3","\u0033\u20E3","\u0034\u20E3","\U0001F1F5"]
    for emoji in emojis:
        await msg.add_reaction(emoji)
    @bot.event
    async def on_reaction_add(reaction, user):
        if reaction.message.id == msg.id and user != bot.user:
            if reaction.emoji == "\u0031\u20E3":
                new = get_standings('stage1')
            elif reaction.emoji == "\u0032\u20E3":
                new = get_standings('stage2')
            elif reaction.emoji == "\u0033\u20E3":
                new = get_standings('stage3')
            elif reaction.emoji == "\u0034\u20E3":
                new = get_standings('stage4')
            elif reaction.emoji == "\U0001F1F5":
                new = get_standings('playoffs')
            await msg.edit(embed=new)
            await msg.remove_reaction(reaction.emoji,user)

for filename in os.listdir('./cogs'):
    bot.load_extension(f'cogs.{filename}')
    print(f'{filename} cog loaded')

try:
    with open('pass.txt') as p:
        secret = p.read()
    bot.run(secret)
except:
    bot.run(os.environ.get('secret_key'))