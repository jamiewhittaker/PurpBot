import discord
from discord.ext import commands

class AC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='ac-birthdays', help='Returns villagers with birthdays')
    async def getBirthdays(self, ctx):
        import requests
        import json

        resp = requests.get('http://acnhapi.com/v1/villagers')

        if resp.ok:
            result = resp.json()

            from datetime import datetime
            now = datetime.now()
            date = f"{now.day}/{now.month}"

            birthdays = []
            for villager in result.values():
                if villager["birthday"] == date:
                    birthdays.append(villager["id"])

            for villager in birthdays:
                embed = getVillagerEmbed(villager)
                await ctx.send(embed=embed)


def getVillagerEmbed(id):
    import requests
    import json

    resp = requests.get('http://acnhapi.com/v1/villagers/' + str(id))
    if resp.ok:
        name = resp.json()["name"]["name-USen"]
        personality = resp.json()["personality"]
        birthdayString = resp.json()["birthday-string"]
        species = resp.json()["species"]
        gender = resp.json()["gender"]
        catchphrase = resp.json()["catch-phrase"]
        image = 'http://acnhapi.com/v1/images/villagers/' + str(id)

        embed = discord.Embed(title=name, color=0xA7D2A4)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Personality", value=personality, inline=False)
        embed.add_field(name="Birthday", value=birthdayString, inline=True)
        embed.add_field(name="Species", value=species, inline=True)
        embed.add_field(name="Gender", value=gender, inline=True)
        embed.add_field(name="Catchphrase", value=catchphrase, inline=True)

        return embed


def setup(bot):
    bot.add_cog(AC(bot))
