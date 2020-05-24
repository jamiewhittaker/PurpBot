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


    @commands.command(name='djenerate', help='Generates a random Djent guitar tab.')
    async def generateDjent(self, ctx):
        import random

        oneString = ""
        for x in range(0, 20):
            randomNum = random.randint(1, 100)

            if randomNum <= 65:
                oneString = oneString + "0  -  "
            if randomNum > 65 and randomNum <= 85:
                oneString = oneString + "1  -  "
            if randomNum > 85 and randomNum <= 95:
                oneString = oneString + "X  -  "

            if randomNum >= 95:
                randomFret = random.randint(2, 24)
                if oneString[-4] == "1":
                    oneString = oneString + "0  -  "
                    oneString = oneString + f"{randomFret}  -  "
                else:
                    oneString = oneString + f"{randomFret}  -  "

        oneString = oneString[:-3]

        randomString = random.randint(1, 100)
        emptyString = ("—" * 32) + "\n"

        output = ""

        if randomString <= 90:
            for x in range(0, 5):
                output = output + emptyString
            output = output + oneString

        if randomString > 90:
            for x in range(0, 4):
                output = output + emptyString
            output = output + oneString
            output = output + f"\n{emptyString}"


        bpm = random.randint(80, 200)
        tuning = ["Drop D","Drop C#","Drop B","Drop A#","Drop F","Drop F#","Drop G"]
        randomTuning = random.choice(tuning)


        embed = discord.Embed(title=f"Your random Djent tab", color=0xC0A886)
        embed.add_field(name=f"{bpm}bpm, {randomTuning}", value=output, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FunCog(bot))
