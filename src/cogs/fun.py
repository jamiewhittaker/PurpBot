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


    @commands.command(name='osrs-stats', help='Gets OSRS Hi-Score data for the given user.')
    async def getOSRS(self, ctx, username):
        import requests

        resp = requests.get('https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + username)
        if resp.ok:
            Overall, Attack, Defence, Strength, Hitpoints, Ranged, Prayer, Magic, Cooking, Woodcutting, Fletching, Fishing, Firemaking, Crafting, Smithing, Mining, Herblore, Agility, Thieving, Slayer, Farming, Runecrafting, Hunter, Construction, *extraWords = resp.text.split("\n")

            skills = {
                "Overall" : {
                    "Rank": Overall.split(",")[0],
                    "Level": Overall.split(",")[1],
                    "Experience": Overall.split(",")[2]
                },
                "Attack" : {
                    "Rank": Attack.split(",")[0],
                    "Level": Attack.split(",")[1],
                    "Experience": Attack.split(",")[2]
                },
                "Defence" : {
                    "Rank": Defence.split(",")[0],
                    "Level": Defence.split(",")[1],
                    "Experience": Defence.split(",")[2]
                },
                "Strength" : {
                    "Rank": Strength.split(",")[0],
                    "Level": Strength.split(",")[1],
                    "Experience": Strength.split(",")[2]
                },
                "Hitpoints" : {
                    "Rank": Hitpoints.split(",")[0],
                    "Level": Hitpoints.split(",")[1],
                    "Experience": Hitpoints.split(",")[2]
                },
                "Ranged" : {
                    "Rank": Ranged.split(",")[0],
                    "Level": Ranged.split(",")[1],
                    "Experience": Ranged.split(",")[2]
                },
                "Prayer" : {
                    "Rank": Prayer.split(",")[0],
                    "Level": Prayer.split(",")[1],
                    "Experience": Prayer.split(",")[2]
                },
                "Magic" : {
                    "Rank": Magic.split(",")[0],
                    "Level": Magic.split(",")[1],
                    "Experience": Magic.split(",")[2]
                },
                "Cooking" : {
                    "Rank": Cooking.split(",")[0],
                    "Level": Cooking.split(",")[1],
                    "Experience": Cooking.split(",")[2]
                },
                "Woodcutting" : {
                    "Rank": Woodcutting.split(",")[0],
                    "Level": Woodcutting.split(",")[1],
                    "Experience": Woodcutting.split(",")[2]
                },
                "Fletching" : {
                    "Rank": Fletching.split(",")[0],
                    "Level": Fletching.split(",")[1],
                    "Experience": Fletching.split(",")[2]
                },
                "Fishing" : {
                    "Rank": Fishing.split(",")[0],
                    "Level": Fishing.split(",")[1],
                    "Experience": Fishing.split(",")[2]
                },
                "Firemaking" : {
                    "Rank": Firemaking.split(",")[0],
                    "Level": Firemaking.split(",")[1],
                    "Experience": Firemaking.split(",")[2]
                },
                "Crafting" : {
                    "Rank": Crafting.split(",")[0],
                    "Level": Crafting.split(",")[1],
                    "Experience": Crafting.split(",")[2]
                },
                "Smithing" : {
                    "Rank": Smithing.split(",")[0],
                    "Level": Smithing.split(",")[1],
                    "Experience": Smithing.split(",")[2]
                },
                "Mining" : {
                    "Rank": Mining.split(",")[0],
                    "Level": Mining.split(",")[1],
                    "Experience": Mining.split(",")[2]
                },
                "Herblore" : {
                    "Rank": Herblore.split(",")[0],
                    "Level": Herblore.split(",")[1],
                    "Experience": Herblore.split(",")[2]
                },
                "Agility" : {
                    "Rank": Agility.split(",")[0],
                    "Level": Agility.split(",")[1],
                    "Experience": Agility.split(",")[2]
                },
                "Thieving" : {
                    "Rank": Thieving.split(",")[0],
                    "Level": Thieving.split(",")[1],
                    "Experience": Thieving.split(",")[2]
                },
                "Slayer" : {
                    "Rank": Slayer.split(",")[0],
                    "Level": Slayer.split(",")[1],
                    "Experience": Slayer.split(",")[2]
                },
                "Farming" : {
                    "Rank": Farming.split(",")[0],
                    "Level": Farming.split(",")[1],
                    "Experience": Farming.split(",")[2]
                },
                "Runecrafting" : {
                    "Rank": Runecrafting.split(",")[0],
                    "Level": Runecrafting.split(",")[1],
                    "Experience": Runecrafting.split(",")[2]
                },
                "Hunter" : {
                    "Rank": Hunter.split(",")[0],
                    "Level": Hunter.split(",")[1],
                    "Experience": Hunter.split(",")[2]
                },
                "Construction" : {
                    "Rank": Construction.split(",")[0],
                    "Level": Construction.split(",")[1],
                    "Experience": Construction.split(",")[2]
                }
            }

            output = ""

            for skill_name, skill_info in skills.items():
                level = skill_info["Level"]
                rank = skill_info["Rank"]
                experience = skill_info["Experience"]
                output = output + f"\n{skill_name}: {level} [{experience} XP]"

            await ctx.send(f"Displaying stats for {username}: \n```{output}```")






def setup(bot):
    bot.add_cog(FunCog(bot))
