import discord
from discord.ext import commands
from discord.ext import tasks

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'Ready {bot.user}')
    print("|    |\__/,|   (`\\")
    print("|  _.|o o  |_   ) )")
    print("|-(((---(((--------")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('jetpackcat.tech'))
    await update_team.start()

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

def player_info(player):
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
    topHeroes = data['competitiveStats']['topHeroes'].items()
    play_time = sorted([[hero, topHero['timePlayed']] for hero, topHero in topHeroes], key=conv)[::-1]
    for hero in play_time:
        if hero[0][:3] in 'anabapbrilúcmermoizen':
            role_info["support"][1].append(hero[0])
        elif hero[0][:3] in 'd.vaorireiroasigwinwreczar':
            role_info["tank"][1].append(hero[0])
        elif len(role_info["damage"][1])<3: 
            role_info["damage"][1].append(hero[0])
    return [player_url,avatar,sr,role_info]

def scrape(player):
    from bs4 import BeautifulSoup
    import requests
    player_url = f"https://www.overbuff.com/players/pc/{'-'.join(player.split('#'))}?mode=competitive"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    s = BeautifulSoup(requests.get(player_url, headers=headers).content, 'html.parser')
    if not (td_list:= s.find_all('td')):
        player_url = f"https://www.overbuff.com/players/pc/{'-'.join(player.split('#'))}"
        s = BeautifulSoup(requests.get(player_url, headers=headers).content, 'html.parser')
        if not (td_list:= s.find_all('td')):
            return player_info(player)
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
        avg = [role_info[role][0] for role in role_info.keys() if role_info[role][0] != 0]
        sr = sum(avg)//len(avg)
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

async def get_team_sr(channel, team : str):
    import requests
    from bs4 import BeautifulSoup
    from multiprocessing import Pool
    from helpers import rankEmoji, hero_dict
    await channel.send("Fetching team...")
    if "gamebattles" in team:
        id = team.split("https://gamebattles.majorleaguegaming.com/pc/overwatch/team/")
        teamMembers = requests.get("https://gb-api.majorleaguegaming.com/api/web/v1/team-members-extended/team/"+id[1]).json()['body']
        teamScreen = requests.get("https://gb-api.majorleaguegaming.com/api/web/v1/team-screen/"+id[1]).json()['body']['teamWithEligibilityAndPremiumStatus']['team']
        teamName = teamScreen['name']
        teamLogo = teamScreen['avatarUrl']
        players = [p['teamMember']['gamertag'].strip('.') for p in teamMembers]
        embed = discord.Embed(title=teamName, url=team, description="Overwatch Collegiate Championship", color=0xff8040)
        embed.set_thumbnail(url=teamLogo)
    else:
        s = requests.get('https://dtmwra1jsgyb0.cloudfront.net/tournaments/5df7969f11f28577f5dd5df7/teams?name={}'.format(team)).json()
        teamUrl = f"https://battlefy.com/teams/{s[0]['persistentTeamID']}"
        logoUrl = s[0]['persistentTeam']['logoUrl']
        name = s[0]['name']
        players = [p['inGameName'] for p in s[0]['players']]
        embed = discord.Embed(title=name, url=teamUrl, description="2020 Overwatch Open Division Season 1 - North America", color=0xff8040)
        embed.set_thumbnail(url=logoUrl)
    highest_avg = []
    average = []
    with Pool(12) as p:
        p_info = p.map(scrape, players)
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
            if heroes:
                hero_emojis = ' '.join(hero_dict[h] for h in heroes)
            else:
                hero_emojis = "N/A"
            highest_avg.append(role_rating)
        else:
            e = "N/A"
            skill_rating = ""
            role_emoji = "N/A"
            role_rank_emoji = ""
            role_rating = ""
            hero_emojis = ""
        embed.add_field(name = f"{player}: {e}{skill_rating}", value = f"{role_emoji} {role_rank_emoji}{role_rating} {hero_emojis}", inline = False)
    if average:
        sorted_highest_avg = sorted(highest_avg)[::-1][:6]
        avg = sum(average)//len(average)
        h_avg = sum(sorted_highest_avg)//len(sorted_highest_avg)
    else: 
        avg = 0
        h_avg = 0
    h_e = rankEmoji(h_avg)
    a_e = rankEmoji(avg)
    embed.add_field(name="Average", value = f"{a_e}{avg}", inline=False)
    embed.add_field(name="Top 6 Players Average", value = f"{h_e}{h_avg}", inline=False)
    embed.set_footer(text="N/A = Player profile private or not yet placed.")
    await channel.send(embed=embed)

@tasks.loop(seconds=60.0)
async def get_matches():
    import datetime
    now = datetime.datetime.now()
    ch = bot.get_channel(546094495448432643)
    if now.isoweekday() == 4:
        await get_team_sr(ch,"Cap'n Crunge")

@bot.command(hidden=True)
async def start_match_scheduler(ctx):
    get_matches.start()
    await ctx.send("Started match scheduler.")

@bot.command(hidden=True)
async def stop_match_scheduler(ctx):
    get_matches.stop()
    await ctx.send("Stopped match scheduler.")

@tasks.loop(hours=1.0)
async def update_team():
    gold_channel = bot.get_channel(661330736913055754)
    black_channel = bot.get_channel(676941215106596864)
    gold_info = team_helper("34049268")
    black_info = team_helper("34064172")
    h_avg_list_gold = [highest for player in gold_info if (highest:=max(list(player[3].values()))[0]) != 0]
    sort_gold = sorted(h_avg_list_gold)[::-1][:6]
    h_gold = sum(sort_gold)//len(sort_gold)
    h_avg_list_black = [highest for player in black_info if (highest:=max(list(player[3].values()))[0]) != 0]
    sort_black = sorted(h_avg_list_black)[::-1][:6]
    h_black = sum(sort_black)//len(sort_black)
    await gold_channel.edit(name=f"💛 Gold Team SR: {h_gold}")
    await black_channel.edit(name=f"🖤 Black Team SR: {h_black}")
    print("loop")

@bot.command(hidden=True)
async def start_update_scheduler(ctx):
    update_team.start()
    await ctx.send("Starting update scheduler...")

@bot.command(hidden=True)
async def stop_update_scheduler(ctx):
    update_team.cancel()
    await ctx.send("Stopping update scheduler...")

@update_team.before_loop
async def before_update_team():
    print("Update scheduler started.")

@update_team.after_loop
async def after_update_team():
    print("Update scheduler ended.")


@get_matches.after_loop
async def after_update_matches():
    print("Match scheduler ended")
    await bot.wait_until_ready()

def team_helper(id : str):
    import requests
    from multiprocessing import Pool
    team_members = requests.get("https://gb-api.majorleaguegaming.com/api/web/v1/team-members-extended/team/"+id).json()['body']
    players = [p['teamMember']['gamertag'].strip('.') for p in team_members]
    with Pool(12) as p:
        p_info = p.map(scrape, players)
    return p_info

@bot.command(aliases=['od'], cog="Competitive")
async def tespa(ctx, team : str):
    ch = ctx.channel
    await get_team_sr(ch,team)

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
