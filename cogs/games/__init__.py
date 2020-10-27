import discord
import random
from discord.ext import commands

cards_dict = {
  1: ["Waterfall","Start chugging and have... "],
  2: ["2 To You","Pick someone to take a drink!"],
  3: ["3 For Me","Take a drink!"],
  4: ["Whores","Ladies, take a drink!"],
  5: ["Never Have I Ever","???"],
  6: ["Dicks","Lads, take a drink!"],
  7: ["Heaven","???"],
  8: ["Date","Pick a player to drink each time you drink."],
  9: ["Rhyme","Choose a word that each player has to rhyme with, starting with the player below you."],
  10: ["Scattergories","Choose a category that each player has to rhyme with, starting with the player below you."],
  11: ["Thumb Master","???"],
  12: ["Question Master","???"],
  13: ["King's Rules","Make a rule or remove another king's rule."]
}

channel = 'https://cdn.discordapp.com/attachments/769777192182743041/'

card_faces = {
    'C':["769991938413166622/CLUB-1.png","769991941139202078/CLUB-2.png","769991943500988426/CLUB-3.png","769991945866182696/CLUB-4.png","769991948270043146/CLUB-5.png","769991891860979742/CLUB-6.png","769991893382987786/CLUB-7.png","769991895132667924/CLUB-8.png","769991896352948264/CLUB-9.png","769991897544392744/CLUB-10.png","769991899255144458/CLUB-11-JACK.png","769991900668887088/CLUB-12-QUEEN.png","769991902753718282/CLUB-13-KING.png"],
    'D':["769993330472779786/DIAMOND-1.png","769993332876509184/DIAMOND-2.png","769993335468195871/DIAMOND-3.png","769993337783451678/DIAMOND-4.png","769993340254158868/DIAMOND-5.png","769993342682529802/DIAMOND-6.png","769993345418133584/DIAMOND-7.png","769993348370268220/DIAMOND-8.png","769993351230914591/DIAMOND-9.png","769993353722331166/DIAMOND-10.png","769993418985963520/DIAMOND-11-JACK.png","769993375914786846/DIAMOND-12-QUEEN.png","769993384332492900/DIAMOND-13-KING.png"],
    'H':["769993910092824586/HEART-1.png","769993914915749948/HEART-2.png","769993918632165426/HEART-3.png","769993922637463582/HEART-4.png","769993926585090078/HEART-5.png","769993930125082634/HEART-6.png","769993933332938792/HEART-7.png","769993937515315240/HEART-8.png","769993888374456351/HEART-9.png","769994014853562388/HEART-10.png","769993999187705886/HEART-11-JACK.png","769994002035900496/HEART-12-QUEEN.png","769994005609709598/HEART-13-KING.png"],
    'S':["769994511283388456/SPADE-1.png","769994514571722782/SPADE-2.png","769994526307123240/SPADE-3.png","769994530941435934/SPADE-4.png","769994535379664907/SPADE-5.png","769994483852509274/SPADE-6.png","769994486683009124/SPADE-7.png","769994490298892308/SPADE-8.png","769994493704404992/SPADE-9.png","769994497597112342/SPADE-10.png","769994500793171968/SPADE-11-JACK.png","769994504513257512/SPADE-12-QUEEN.png","769994507671306270/SPADE-13-KING.png"],
    '$':["769996608367493161/JOKER-1.png","769996606854135818/JOKER-3.png"]
}

class Deck(object):
        """docstring for Deck"""
        def __init__(self, enable_joker=False):
            super(Deck, self).__init__()
            self.cards = []
            self.build(enable_joker)

        def build(self, enable_joker):
            self.cards = [(v, s) for v in range (1, 14) for s in ["S", "C", "D", "H"]]
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

    def create_embed(self,card):
        embed = discord.Embed(title=cards_dict[card][0],description=f"```yaml\n{cards_dict[card][1]}\n```")
        embed.set_footer(text="Circle of Death",icon_url="https://cdn.discordapp.com/attachments/659602898585518100/769760580554457098/plastic-cup.png")
        return embed

    @commands.command()
    async def kc(self, ctx, *args): 
        args = list(args)
        if not args:
            card = self.decks[0].pop()
            embed = self.create_embed(card[0])
            embed.set_thumbnail(url=channel+card_faces[card[1]][card[0]-1])
            await ctx.send(embed=embed)
        elif args[0] == 'new':
            self.decks[0] = Deck(True if args[-1] == 'joker' else False)
            self.decks[0].shuffle()
            await ctx.send('Created a new shuffled deck')

def setup(bot):
    bot.add_cog(Games(bot))