import discord
from discord.ext import commands

class ACNH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='acnh-birthdays', help='Returns villagers with birthdays')
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


    @commands.command(name='acnh-villager', help='Returns villager from name')
    async def getVillager(self, ctx, *args):
        import requests
        import json

        searchTerm = " ".join(args[:]).strip()

        if not searchTerm:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!acnh-villager Roald` or `!acnh-fish Ketchup`")
            raise Exception("User passed no parameters")

        resp = requests.get('http://acnhapi.com/v1/villagers')

        if resp.ok:
            result = resp.json()

            found = False
            for villager in result.values():
                if villager["name"]["name-USen"].lower() == searchTerm.lower():
                    found = True
                    embed = getVillagerEmbed(villager["id"])
                    await ctx.send(embed=embed)

            if not found:
                await ctx.send("Villager not found. Please check your spelling.")



    @commands.command(name='acnh-fish', help='Returns fish from name')
    async def getFish(self, ctx, *args):
        import requests
        import json

        searchTerm = " ".join(args[:]).strip()

        if not searchTerm:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!acnh-fish bitterling` or `!acnh-fish sea bass`")
            raise Exception("User passed no parameters")

        resp = requests.get('http://acnhapi.com/v1/fish')

        found = False
        if resp.ok:
            result = resp.json()

            for fish in result.values():
                if fish["name"]["name-USen"].lower() == searchTerm.lower():
                    found = True
                    embed = getFishEmbed(fish["id"])
                    await ctx.send(embed=embed)

            if not found:
                await ctx.send("Fish not found. Please check your spelling.")


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
        embed.add_field(name="Personality", value=personality, inline=True)
        embed.add_field(name="Species", value=species, inline=True)
        embed.add_field(name="Gender", value=gender, inline=True)
        embed.add_field(name="Birthday", value=birthdayString, inline=True)
        embed.add_field(name="Catchphrase", value=catchphrase, inline=False)

        return embed


def getFishEmbed(id):
    import requests
    import json

    resp = requests.get('http://acnhapi.com/v1/fish/' + str(id))
    if resp.ok:
        name = resp.json()["name"]["name-USen"]
        image = resp.json()["icon_uri"]
        location = resp.json()["availability"]["location"]
        rarity = resp.json()["availability"]["rarity"]
        price = resp.json()["price"]
        priceCJ = resp.json()["price-cj"]


        embed = discord.Embed(title=name, color=0xA7D2A4)
        embed.set_thumbnail(url=image)

        embed.add_field(name="Location", value=location, inline=True)
        embed.add_field(name="Rarity", value=rarity, inline=True)
        embed.add_field(name="Price", value=price, inline=True)

        if not resp.json()["availability"]["isAllYear"]:
            northern = resp.json()["availability"]["month-northern"]
            southern = resp.json()["availability"]["month-southern"]
            embed.add_field(name="Northern Hemisphere months", value=northern, inline=True)
            embed.add_field(name="Southern Hemisphere months", value=southern, inline=True)
        else:
            embed.add_field(name="Availability", value="All Year", inline=True)

        if not resp.json()["availability"]["isAllDay"]:
            times = resp.json()["availability"]["time"]
            embed.add_field(name="Times", value=times, inline=True)
        else:
            embed.add_field(name="Times", value="All Day", inline=True)


        embed.add_field(name="Price (C.J.)", value=priceCJ, inline=True)

        catchphrase = resp.json()["catch-phrase"]
        museum = resp.json()["museum-phrase"]

        embed.add_field(name="Catchphrase", value=catchphrase, inline=True)
        embed.add_field(name="Museum phrase", value=museum, inline=False)

        return embed


def setup(bot):
    bot.add_cog(ACNH(bot))
