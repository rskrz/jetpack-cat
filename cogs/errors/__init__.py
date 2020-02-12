import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        ignored = (commands.CommandNotFound)

        msg = "Please message <@73578715598032896> for assistance."
        response = f"{error} {msg}"

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.UserInputError):
            await ctx.send(response)

        elif isinstance(error, commands.BadArgument):
            await ctx.send(response)

        elif isinstance(error,commands.CommandInvokeError):
            cmd = ctx.command.qualified_name
            if cmd == "sr":
                await ctx.send(f"User not found. {msg}")
            elif cmd == "tespa":
                await ctx.send(f"Team not found. {msg}")
        
        else:
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))