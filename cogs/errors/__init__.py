import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def msger(self, item, cmd):
        return f"{item} not found. Please try \".help {cmd}\" or message <@73578715598032896> for assistance."
    
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
                await ctx.send(self.msger("User", cmd))
            elif cmd == "tespa":
                await ctx.send(self.msger("Team", cmd))
            elif cmd == "od":
                await ctx.send(self.msger("Team", cmd))
        
        else:
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))