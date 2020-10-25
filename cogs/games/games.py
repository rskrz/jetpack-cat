import discord
from discord.ext import commands

class Games(commands.Cog):
	class Deck(object):
		"""docstring for Deck"""
		def __init__(self, enable_joker=False):
			super(Deck, self).__init__()
			self.cards = []
			self.build(enable_joker)

		def build(self, enable_joker):
			face_mappings = {1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K'}
			self.cards = [(face_mappings[v], s) for v in range (1, 14) for s in ["S", "C", "D", "H"]]
			if enable_joker:
				self.cards += [('$', '$'), ('$', '$')]

		def shuffle(self):
			return random.shuffle(self.cards)

		def pop(self):
			return self.cards.pop(0)
			
    def __init__(self,bot):
        self.bot = bot
        self.decks = [None]

    @commands.command():
    async def kc(self, ctx, *args):
    	if args:
    		pass

    	elif args[0] == 'new':
    		self.decks[0] = Deck(True if args[1] == 'joker' else False)
    		self.decks[0].shuffle()
    		await ctx.send('Created a new shuffled deck')

    	elif args[0] == 'help':
    		embed = discord.Embed(description="This is the help screen")
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/659602898585518100/769760580554457098/plastic-cup.png")
    		await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Games(bot))