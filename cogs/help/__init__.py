import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        bot.remove_command("help")

    @commands.command()
    async def help(self, ctx, *args):
        cmd = args[0].strip(".") if args else "help"
        url = "https://jetpackcat.tech"
        c = 0xff8040

        if cmd == "help":
            embed = discord.Embed(
                title="Help",
                url=url,
                description="Type .help <command> to show command information.",
                color=c
            )
            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url
            )
            value = """
            ```
            .sr Get player role SR\n
            .rank Get Player Rank\n
            ```
            """
            embed.add_field(
                name="Competitive", 
                value=(
                    "```"
                    ".sr            Get player role SR\n"
                    ".rank          Get player hero ranks\n"
                    ".tespa         Get tespa team SR\n"
                    ".od            Get Open Division team SR\n"
                    "```"
                ),
                inline=False
            )
            embed.add_field(
                name="Overwatch League",
                value=(
                    "```"
                    ".team          Get OWL team info\n"
                    ".stats         Get OWL player info\n"
                    ".compare       Compare two OWL players\n"
                    ".standings     Get OWL standings\n"
                    ".schedule      Get OWL schedule\n"
                    "```"
                ),
                inline=False)
            embed.add_field(
                name="General",
                value=(
                    "```"
                    ".hero          Generate a random hero\n"
                    ".role          Generate a random role\n"
                    ".help          Shows this message\n"
                    "```"
                ),
                inline=False
            )
            return await ctx.send(embed=embed)
        elif cmd == "sr":
            usage = ".sr <player>"
            example = ".sr skrz#11924"
            embed = discord.Embed(
                title="Player Name",
                url=url,
                description="Average role SR",
                color=c
            )
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Overwatch_circle_logo.svg/1200px-Overwatch_circle_logo.svg.png")
            embed.add_field(name="<:Tank:619262646885154846> Tank SR", value="Tank heroes", inline=False)
            embed.add_field(name="<:Dps:619262646834692106> DPS SR", value="DPS heroes", inline=False)
            embed.add_field(name="<:Support:619262646708863007> Support SR", value="Support heroes", inline=False)
        elif cmd == "tespa":
            usage = ".[tespa|od] <team>"
            example = ".tespa https://gamebattles.majorleaguegaming.com/pc/overwatch/team/34049268"
            embed = discord.Embed(
                title="Team Name", 
                url=url, 
                description="Active Tournament", 
                color=c
            )
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Overwatch_circle_logo.svg/1200px-Overwatch_circle_logo.svg.png")
            embed.add_field(name="Player#1234: Average role SR", value="Highest role SR: Top role heroes", inline=False)
            embed.add_field(name="Average", value="Average of each player's average role SR", inline=False)
            embed.add_field(name="Top 6 Players Average", value="Average of top 6 player's highest role SR", inline=False)
            embed.set_footer(text="N/A = Player profile private or not yet placed.")
        
        content = f"```Usage:\n{usage}\n\nExample:\n{example}```"
                
        await ctx.send(content=content,embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
            