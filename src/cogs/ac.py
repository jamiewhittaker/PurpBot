import discord
from discord.ext import commands
import requests
import json

class ACNH(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='acnh-birthdays', help='Returns villagers with birthdays')
    async def getBirthdays(self, ctx):
        resp = requests.get('http://acnhapi.com/v1/villagers')
        if resp.ok:
            from datetime import datetime
            result = resp.json()
            now = datetime.now()
            date = f"{now.day}/{now.month}"

            birthdays = []
            for villager in result.values():
                if villager["birthday"] == date:
                    birthdays.append(villager["id"])

            if not birthdays:
                await ctx.send("No villagers have birthdays today.")

            for villager in birthdays:
                embed = getVillagerEmbed(villager)
                await ctx.send(embed=embed)


    @commands.command(name='acnh-villager', help='Returns villager from name')
    async def getVillager(self, ctx, *args):
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
        searchTerm = " ".join(args[:]).strip()

        if not searchTerm:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!acnh-fish bitterling` or `!acnh-fish sea bass`")
            raise Exception("User passed no parameters")

        resp = requests.get('http://acnhapi.com/v1/fish')

        if resp.ok:
            result = resp.json()
            found = False

            for fish in result.values():
                if fish["name"]["name-USen"].lower() == searchTerm.lower():
                    found = True
                    embed = getFishEmbed(fish["id"])
                    await ctx.send(embed=embed)

            if not found:
                await ctx.send("Fish not found. Please check your spelling.")


    @commands.command(name='acnh-bug', help='Returns bug from name')
    async def getBug(self, ctx, *args):
        searchTerm = " ".join(args[:]).strip()

        if not searchTerm:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!acnh-bug tarantula` or `!acnh-bug common butterfly`")
            raise Exception("User passed no parameters")

        resp = requests.get('http://acnhapi.com/v1/bugs')

        if resp.ok:
            result = resp.json()
            found = False

            for bug in result.values():
                if bug["name"]["name-USen"].lower() == searchTerm.lower():
                    found = True
                    embed = getBugEmbed(bug["id"])
                    await ctx.send(embed=embed)

            if not found:
                await ctx.send("Bug not found. Please check your spelling.")



    @commands.command(name='acnh-fossil', help='Returns fossil from name')
    async def getFossil(self, ctx, *args):
        searchTerm = " ".join(args[:]).strip()

        if not searchTerm:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!acnh-fossil amber` or `!acnh-bug diplo skull`")
            raise Exception("User passed no parameters")

        embed = getFossilEmbed(searchTerm)
        if embed:
            found = True
            await ctx.send(embed=embed)
        else:
            await ctx.send("Fossil not found. Please check your spelling.")


def getVillagerEmbed(id):
    resp = requests.get('http://acnhapi.com/v1/villagers/' + str(id))
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["image_uri"])
        embed.add_field(name="Personality", value=resp.json()["personality"], inline=True)
        embed.add_field(name="Species", value=resp.json()["species"], inline=True)
        embed.add_field(name="Gender", value=resp.json()["gender"], inline=True)
        embed.add_field(name="Birthday", value=resp.json()["birthday-string"], inline=True)
        embed.add_field(name="Catchphrase", value=resp.json()["catch-phrase"], inline=False)

        return embed


def getFishEmbed(id):
    resp = requests.get('http://acnhapi.com/v1/fish/' + str(id))
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["icon_uri"])

        embed.add_field(name="Location", value=resp.json()["availability"]["location"], inline=True)
        embed.add_field(name="Rarity", value=resp.json()["availability"]["rarity"], inline=True)
        embed.add_field(name="Price", value=resp.json()["price"], inline=True)

        if not resp.json()["availability"]["isAllYear"]:
            embed.add_field(name="Northern Hemisphere months", value=resp.json()["availability"]["month-northern"], inline=True)
            embed.add_field(name="Southern Hemisphere months", value=resp.json()["availability"]["month-southern"], inline=True)
        else:
            embed.add_field(name="Availability", value="All Year", inline=True)

        if not resp.json()["availability"]["isAllDay"]:
            embed.add_field(name="Times", value=resp.json()["availability"]["time"], inline=True)
        else:
            embed.add_field(name="Times", value="All Day", inline=True)

        embed.add_field(name="Price (C.J.)", value=resp.json()["price-cj"], inline=True)
        embed.add_field(name="Catchphrase", value=resp.json()["catch-phrase"], inline=True)
        embed.add_field(name="Museum phrase", value=resp.json()["museum-phrase"], inline=False)

        return embed


def getBugEmbed(id):
    resp = requests.get('http://acnhapi.com/v1/bugs/' + str(id))
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["icon_uri"])

        embed.add_field(name="Location", value=resp.json()["availability"]["location"], inline=True)
        embed.add_field(name="Rarity", value=resp.json()["availability"]["rarity"], inline=True)
        embed.add_field(name="Price", value=resp.json()["price"], inline=True)

        if not resp.json()["availability"]["isAllYear"]:
            embed.add_field(name="Northern Hemisphere months", value=resp.json()["availability"]["month-northern"], inline=True)
            embed.add_field(name="Southern Hemisphere months", value=resp.json()["availability"]["month-southern"], inline=True)
        else:
            embed.add_field(name="Availability", value="All Year", inline=True)

        if not resp.json()["availability"]["isAllDay"]:
            embed.add_field(name="Times", value=resp.json()["availability"]["time"], inline=True)
        else:
            embed.add_field(name="Times", value="All Day", inline=True)

        embed.add_field(name="Price (Flick)", value=resp.json()["price-flick"], inline=True)
        embed.add_field(name="Catchphrase", value=resp.json()["catch-phrase"], inline=True)
        embed.add_field(name="Museum phrase", value=resp.json()["museum-phrase"], inline=False)

        return embed


def getFossilEmbed(name):
    resp = requests.get('http://acnhapi.com/v1/fossils/' + name.replace(" ", "_"))
    if resp.ok:
        embed = discord.Embed(title=resp.json()["name"]["name-USen"], color=0xA7D2A4)
        embed.set_thumbnail(url=resp.json()["image_uri"])
        embed.add_field(name="Price", value=resp.json()["price"], inline=True)
        embed.add_field(name="Museum phrase", value=resp.json()["museum-phrase"], inline=False)
        return embed

def setup(bot):
    bot.add_cog(ACNH(bot))
