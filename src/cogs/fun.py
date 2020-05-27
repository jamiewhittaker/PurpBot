import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Quotes are fetched from each line of the .txt file and a random line is sent.
    @commands.command(name='quote', help='Responds with a quote')
    async def get_quote(self, ctx):
        import random
        with open('files/quotes.txt') as f:
            lines = f.readlines()
            response = random.choice(lines)
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
        for x in range(0, 14):
            randomNum = random.randint(1, 100)

            if randomNum <= 65:
                oneString = oneString + "0\t—\t"
            if randomNum > 65 and randomNum <= 85:
                oneString = oneString + "1\t—\t"
            if randomNum > 85 and randomNum <= 95:
                oneString = oneString + "X\t—\t"

            if randomNum >= 95:
                randomFret = random.randint(2, 24)
                if oneString:
                    if oneString[-4] == "1":
                        oneString = oneString + "0\t—\t"
                        oneString = oneString + f"{randomFret}\t—\t"
                    else:
                        oneString = oneString + f"{randomFret}\t—\t"
                else:
                    oneString = oneString + f"{randomFret}\t—\t"

        oneString = oneString[:-3]

        emptyString = ("—\t" * 24) + "\n"
        output = ""
        randomString = random.randint(1, 100)

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
        randomTuning = random.choice(["Drop D","Drop C#","Drop B","Drop A#","Drop F","Drop F#","Drop G"])

        embed = discord.Embed(title=f"Your random Djent tab", color=0xff0000)
        embed.set_thumbnail(url="https://cdn.playlists.net/images/playlists/image/medium/82282.jpg")
        embed.add_field(name=f"{bpm}bpm, {randomTuning}", value=output, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
