import discord
from discord.ext import commands
from helpers import teams, hero_dict

class Owl(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def owl_team(self, team_id):
        import requests
        from datetime import datetime
        from pytz import timezone
        url = "https://api.overwatchleague.com/v2/teams/"+team_id+"?expand=article,schedule&locale=en_US"
        data = requests.get(url).json()
        output = []
        win = data['data']['records']['matchWin']
        loss = data['data']['records']['matchLoss']
        record = f"{win}W - {loss}L"
        output.append(record)
        matches = []
        for match in data['data']['schedule']:
            matchInfo = {}
            team1 = match['competitors'][0]['abbreviatedName']
            team2 = match['competitors'][1]['abbreviatedName']
            date = datetime.fromtimestamp(match['startDate']/1000.0).astimezone(timezone('US/Central')).strftime('%a %b %d %I:%M:%S %p')
            upcoming = (team1,team2)
            matchInfo[upcoming] = date
            matches.append(matchInfo)
        output.append(matches)
        teamPlayers = []
        for player in data['data']['players']:
            playerInfo = {}
            playerName = player['name']
            playerRole = player['role']
            playerInfo[playerName] = playerRole
            teamPlayers.append(playerInfo)
        output.append(teamPlayers)
        return output

    @commands.command()
    async def team(self, ctx, teamName):
        teamName = teamName.lower()
        team1 = next(value for key, value in teams.items() if teamName in key)
        teamId =  team1[4]
        teamInfo = await self.owl_team(teamId)
        desc = teamInfo[0]
        teamMatches = teamInfo[1]
        teamPlayers = teamInfo[2]
        embed = discord.Embed(title=team1[0]+team1[3],url="https://overwatchleague.com/en-us/teams/"+teamId,description=desc,color=team1[1])
        for match in teamMatches:
            team1 = list(match.keys())[0][0]
            team2 = list(match.keys())[0][1]
            team1_info = next(value for key, value in teams.items() if team1 in key)
            team2_info = next(value for key, value in teams.items() if team2 in key)
            teamTitle = f"{team1} {team1_info[3]} vs {team2 } {team2_info[3]}"
            teamDesc = list(match.values())[0]
            embed.add_field(name=teamTitle,value=teamDesc,inline=True)
        for player in teamPlayers:
            playerName = list(player.keys())[0]
            playerRole = list(player.values())[0]
            playerRole = playerRole.capitalize()
            embed.add_field(name=playerName,value=playerRole,inline=True)
        await ctx.send(embed=embed)

    def sortSecond(self, val):
        return val[1]

    async def player_stats(self, name):
        import requests
        url = 'https://api.overwatchleague.com/stats/players?stage_id=regular_season&season=2019'
        data = requests.get(url).json()
        for player in data['data']:
            if player['name'].lower() == name.lower():
                player_url = "https://api.overwatchleague.com/players/"+str(player['playerId'])+"?locale=en-us&season=2019&stage_id=regular_season&expand=stats,stat.ranks"
                playerData = requests.get(player_url).json()
                #playerInfo = []
                picture = playerData['data']['player']['headshot']
                playerHeroes = []
                for hero in playerData['data']['stats']['heroes']:
                    heroArray = [hero['name'],hero['stats']['time_played_total']]
                    playerHeroes.append(heroArray)
                    playerHeroes.sort(key = self.sortSecond, reverse = True)
                heroes = playerHeroes[:3]
                return(player,picture,heroes)

    @commands.command(description='get player stats', aliases=['player'])
    async def stats(self, ctx, name : str):
        playerStats,playerPicture,playerHeroes = await self.player_stats(name)
        hours = playerStats['time_played_total']//3600
        minutes = (playerStats['time_played_total']%3600)//60
        time_played = f"{round(hours)}h {round(minutes)}m"
        playerTeam = next(value for key, value in teams.items() if playerStats['team'] in key)
        desc = f"{str(playerStats['role']).capitalize()} player for {playerTeam[3]}"
        emojis = ""
        for hero in playerHeroes:
            emojis += hero_dict[hero[0]]
        embed = discord.Embed(title=str(playerStats['name']), url = "https://overwatchleague.com/en-us/players/"+str(playerStats['playerId']), description=desc, color=playerTeam[1])
        embed.set_thumbnail(url=playerPicture)
        embed.add_field(name="ELIM", value=str(round(playerStats['eliminations_avg_per_10m'],2)), inline=True)
        embed.add_field(name="DEATHS", value=str(round(playerStats['deaths_avg_per_10m'],2)), inline=True)
        embed.add_field(name="K/D", value=str(round(playerStats['eliminations_avg_per_10m']/playerStats['deaths_avg_per_10m'],2)), inline=True)
        embed.add_field(name="DAMAGE", value=str(round(playerStats['hero_damage_avg_per_10m'])), inline=True)
        embed.add_field(name="HEALING", value=str(round(playerStats['healing_avg_per_10m'])), inline=True)
        embed.add_field(name="ULTIMATES", value=str(round(playerStats['ultimates_earned_avg_per_10m'],2)), inline=True)
        embed.add_field(name="FINAL BLOWS", value=str(round(playerStats['final_blows_avg_per_10m'],2)), inline=True)
        embed.add_field(name="TIME PLAYED", value=time_played, inline=True)
        embed.add_field(name="HEROES",value=emojis,inline=True)
        embed.set_footer(text="All stats are avg. per 10 minutes unless otherwise noted.")
        await ctx.send(embed=embed)

    @commands.command(desc="compare player stats")
    async def compare(self, ctx, player1 : str, player2 : str):
        playerStats,playerPicture,playerData = await self.player_stats(player1)
        playerStats2,playerPicture2,player2Data = await self.player_stats(player2)
        hours = playerStats['time_played_total']//3600
        hours2 = playerStats2['time_played_total']//3600
        minutes = (playerStats['time_played_total']%3600)//60
        minutes2 = (playerStats2['time_played_total']%3600)//60
        playerTeam = next(value for key, value in teams.items() if playerStats['team'] in key)
        playerTeam2 = next(value for key, value in teams.items() if playerStats2['team'] in key)
        time_played = f"{round(hours)}h {round(minutes)}m"
        time_played2 = f"{round(hours2)}h {round(minutes2)}m"
        desc = f"{playerStats['role'].capitalize()} player for {playerTeam[3]}"
        desc2 = f"{playerStats2['role'].capitalize()} player for {playerTeam2[3]}"
        embed = discord.Embed(title="Player Stats Comparison", url = "https://overwatchleague.com/en-us/stats",color=0xff8900)
        embed.set_thumbnail(url="https://www.plusforward.net/files/2016/15919/1_ow-league.png")
        embed.add_field(name=playerStats['name'],value=desc,inline=True)
        embed.add_field(name=playerStats2['name'],value=desc2,inline=True)
        embed.add_field(name="ELIM", value=str(round(playerStats['eliminations_avg_per_10m'],2)), inline=True)
        embed.add_field(name="ELIM", value=str(round(playerStats2['eliminations_avg_per_10m'],2)), inline=True)
        embed.add_field(name="DEATHS", value=str(round(playerStats['deaths_avg_per_10m'],2)), inline=True)
        embed.add_field(name="DEATHS", value=str(round(playerStats2['deaths_avg_per_10m'],2)), inline=True)
        embed.add_field(name="K/D", value=str(round(playerStats['eliminations_avg_per_10m']/playerStats['deaths_avg_per_10m'],2)), inline=True)
        embed.add_field(name="K/D", value=str(round(playerStats2['eliminations_avg_per_10m']/playerStats2['deaths_avg_per_10m'],2)), inline=True)
        embed.add_field(name="DAMAGE", value=str(round(playerStats['hero_damage_avg_per_10m'])), inline=True)
        embed.add_field(name="DAMAGE", value=str(round(playerStats2['hero_damage_avg_per_10m'])), inline=True)
        embed.add_field(name="HEALING", value=str(round(playerStats['healing_avg_per_10m'])), inline=True)
        embed.add_field(name="HEALING", value=str(round(playerStats2['healing_avg_per_10m'])), inline=True)
        embed.add_field(name="ULTIMATES", value=str(round(playerStats['ultimates_earned_avg_per_10m'],2)), inline=True)
        embed.add_field(name="ULTIMATES", value=str(round(playerStats2['ultimates_earned_avg_per_10m'],2)), inline=True)
        embed.add_field(name="FINAL BLOWS", value=str(round(playerStats['final_blows_avg_per_10m'],2)), inline=True)
        embed.add_field(name="FINAL BLOWS", value=str(round(playerStats2['final_blows_avg_per_10m'],2)), inline=True)
        embed.add_field(name="TIME PLAYED", value=time_played, inline=True)
        embed.add_field(name="TIME PLAYED", value=time_played2, inline=True)
        embed.set_footer(text="All stats are avg. per 10 minutes unless otherwise noted.")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Owl(bot))