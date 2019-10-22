import discord
from discord.ext import commands

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
    from helpers import teams
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
    from helpers import teams
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

def playerInfo(player):
    import requests
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

@bot.command(aliases=['od'])
async def tespa(ctx, team : str):
    import requests
    from bs4 import BeautifulSoup
    from multiprocessing import Pool
    from helpers import rankEmoji, hero_dict
    await ctx.send("Fetching team...")
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
    with Pool(12) as p:
        p_info = p.map(playerInfo, players)
    for i in range(len(p_info)):
        skill_rating, role_info = p_info[i][2:]
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

async def run_bot():
    import os
    for filename in os.listdir('./cogs'):
        bot.load_extension(f'cogs.{filename}')
        print(f'{filename} cog loaded')
    try:
        with open('pass.txt') as p:
            secret = p.read()
        await bot.start(secret)
    except:
        await bot.start(os.environ.get('secret_key'))

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
