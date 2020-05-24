import discord
from discord.ext import commands

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Quotes are fetched from each line of the .txt file and a random line is sent.
    @commands.command(name='quote', help='Responds with one of Liam\'s timeless quotes')
    async def get_liamism(self, ctx):
        import random
        with open('quotes.txt') as f:
            lines = f.readlines()
            response = random.choice(lines) + ' <:sexy:713081212503195821>'
            await ctx.send(response)


    @commands.command(name='rng', help='Generates a random number between 1 and the given value.')
    async def getRandomNum(self, ctx, end_number):
        if end_number.isdigit():
            if int(end_number) > 0:
                import random
                response = random.randint(1, int(end_number))
                await ctx.send(response)
            else:
                await ctx.send("Invalid parameter, must be a digit greater than 0.")
        else:
            await ctx.send("Invalid parameter, must be a digit greater than 0.")


    

def setup(bot):
    bot.add_cog(FunCog(bot))
