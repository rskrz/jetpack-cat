import discord
from discord.ext import commands

class PDF(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def pdf(self, ctx, title):
        import img2pdf
        import os

        files = ctx.message.attachments
        output = []

        for file in files:
            await file.save(file_name:= (f"cogs/PDF/input/{file.filename}"))
            output.append(file_name)

        with open(pdf_name:= (f"cogs/PDF/output/{title}.pdf"),"wb") as f:
            f.write(img2pdf.convert(output))

        file = discord.File(pdf_name, filename=f"{title}.pdf")
        await ctx.send(file=file)

        for file in files:
            os.remove(f"cogs/PDF/input/{file.filename}")
        os.remove(pdf_name)

def setup(bot):
    bot.add_cog(PDF(bot))