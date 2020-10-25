import discord
import random
from discord.ext import commands

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

class Games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.decks = [None]

    @commands.command()
    async def kc(self, ctx, *args): 
        args = list(args)
        if not args:
            await ctx.send(''.join(self.decks[0].pop()))
        elif args[0] == 'new':
            self.decks[0] = Deck(True if args[-1] == 'joker' else False)
            self.decks[0].shuffle()
            await ctx.send('Created a new shuffled deck')

def setup(bot):
    bot.add_cog(Games(bot))