import discord
from discord.ext import commands
import requests
import json
import helper.ac_helper as ac

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
                embed = ac.getVillagerEmbed(villager)
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
                    embed = ac.getVillagerEmbed(villager["id"])
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
                    embed = ac.getFishEmbed(fish["id"])
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
                    embed = ac.getBugEmbed(bug["id"])
                    await ctx.send(embed=embed)

            if not found:
                await ctx.send("Bug not found. Please check your spelling.")



    @commands.command(name='acnh-fossil', help='Returns fossil from name')
    async def getFossil(self, ctx, *args):
        searchTerm = " ".join(args[:]).strip()


        if not searchTerm:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!acnh-fossil amber` or `!acnh-fossil diplo skull`")
            raise Exception("User passed no parameters")

        embed = ac.getFossilEmbed(searchTerm)
        if embed:
            found = True
            await ctx.send(embed=embed)
        else:
            await ctx.send("Fossil not found. Please check your spelling.")


    @commands.command(name='acnh-music', help='Returns KK Slider music item from name')
    async def getMusic(self, ctx, *args):
        searchTerm = " ".join(args[:]).strip()
        if not searchTerm:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!acnh-music Agent K.K.` or `!acnh-music K.K. Metal`")
            raise Exception("User passed no parameters")

        resp = requests.get('http://acnhapi.com/v1/songs')

        if resp.ok:
            result = resp.json()
            found = False

            for song in result.values():
                if song["name"]["name-USen"].lower() == searchTerm.lower():
                    found = True
                    embed = ac.getSongEmbed(song["id"])
                    await ctx.send(embed=embed)

            if not found:
                await ctx.send("Song not found. Please check your spelling.")

def setup(bot):
    bot.add_cog(ACNH(bot))
