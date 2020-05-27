import discord
from discord.ext import commands

class OSRS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='osrs-xpto99', help='Returns the XP needed to get a skill to 99')
    async def getXPto99(self, ctx, *args):

        parameters = " ".join(args[:]).split(",")
        usernames = []
        for parameter in parameters:
            usernames.append(parameter.strip())

        if not usernames[0]:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!osrs-xpto99 Zezima` or `!osrs-xpto99 Zezima, Lynx Titan`")
            raise Exception("User passed no parameters")

        if len(usernames) > 2:
            await ctx.send("This command currently only accepts two parameters.")
            raise Exception("User tried to use more than two parameters")

        for username in usernames:
            if getOSRS(username) == False:
                await ctx.send(f"Could not find {username} in the Hi-Scores")
                raise Exception("User searched for invalid username")


        def getOutput(username):
            skills = getOSRS(username)

            if skills:
                output = ""
                for skill_name, skill_info in skills.items():
                    level = skill_info["Level"]

                    if skill_name == "Overall":
                        output += f"\n**{skill_name}**: {level}"
                    else:
                        if int(skill_info["Experience"]) > 13034431:
                            output += f"\n**{skill_name}**: {level} [Already 99]"
                        else:
                            experience = 13034431 - int(skill_info["Experience"])
                            experience = f"{int(experience):,d}"
                            output += f"\n**{skill_name}**: {level} [{experience} XP]"


                embed.add_field(name=f"{username}", value=output, inline=True)


        if len(usernames) == 1:
            embed = discord.Embed(title=f"Stats for {usernames[0]}", description="Stats fetched from OSRS Hi-Scores.", color=0xC0A886)
            getOutput(usernames[0])

        if len(usernames) == 2:
            embed = discord.Embed(title=f"Stats for {usernames[0]} and {usernames[1]}", description="Stats fetched from OSRS Hi-Scores.", color=0xC0A886)
            getOutput(usernames[0])
            getOutput(usernames[1])

        embed.set_thumbnail(url="https://lh3.googleusercontent.com/5Dj_vzUhLURKE7dnDElvo9lbgzaMynzT0tyyvStQUt3pSZ8Ub0jzsa05oVy4EtHjEq8=s180-rw")
        await ctx.send(embed=embed)

        

    @commands.command(name='osrs-itemID', help='Returns the Item ID for the item searched')
    async def getOSRSItemID(self, ctx, *args):
        searchTerm = " ".join(args[:])
        itemID = getItemID(searchTerm)
        await ctx.send(itemID)


    @commands.command(name='osrs-pc', help='Returns Grand Exchange information for an item')
    async def getOSRSGEPrice(self, ctx, *args):
        import requests
        import json

        searchTerm = " ".join(args[:])
        itemID = getItemID(searchTerm)

        if not itemID:
            await ctx.send("Item does not exist.")
            raise Exception(f"{searchTerm} was not found in the OSRSBox items JSON.")

        resp = requests.get('http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' + str(itemID))

        if resp.ok:
            resp2 = requests.get("https://api.osrsbox.com/items?where={%22id%22:%22" + str(itemID) + "%22}")

            embed = discord.Embed(title=resp.json()["item"]["name"], color=0xC0A886)
            embed.set_thumbnail(url=resp.json()["item"]["icon_large"])
            embed.add_field(name="Description", value=resp.json()["item"]["description"], inline=False)
            embed.add_field(name="Current price", value=resp.json()["item"]["current"]["price"], inline=True)

            if resp2.ok:
                embed.add_field(name="Low alch value", value=resp2.json()["_items"][0]["lowalch"], inline=True)
                embed.add_field(name="High alch value", value=resp2.json()["_items"][0]["highalch"], inline=True)
                embed.add_field(name="Buy limit", value=resp2.json()["_items"][0]["buy_limit"], inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Could not find item in the Grand Exchange.")


    @commands.command(name='osrs-wiki', help='Searches OSRS Wiki for the given term.')
    async def getOSRSWiki(self, ctx, *args):
        import requests
        import json

        searchTermFixed = " ".join(args[:])
        searchTermFixed = searchTermFixed.replace(" ", "_")
        resp = requests.get('https://oldschool.runescape.wiki/api.php?action=opensearch&search=' + searchTermFixed)

        if resp.ok:
            topResult = resp.json()[1][0]
            topResultLink = resp.json()[3][0]

            resp2 = requests.get('https://oldschool.runescape.wiki/api.php?action=query&exlimit=1&explaintext=1&exintro=1&format=json&formatversion=2&prop=extracts&titles=' + topResult)

            if resp2.ok:
                result = resp2.json()
                extract = result['query']['pages'][0]['extract']

                if not extract:
                    await ctx.send(content=f"Showing result for: {topResult}\nRead here: <{topResultLink}>")
                else:
                    extract = extract.splitlines()[0]
                    if len(extract) > 1021:
                        extract = (extract[:1021] + '...')

                    embed = discord.Embed(title=f"{topResult}", url=topResultLink, color=0xC0A886)
                    embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/thumb/c/c3/Wiki_Integration_%281%29.png/200px-Wiki_Integration_%281%29.png?d07a4")
                    embed.add_field(name="Summary (first paragraph)", value=extract, inline=False)
                    embed.add_field(name="Read more:", value=str(topResultLink), inline=False)
                    await ctx.send(embed=embed)



    @commands.command(name='osrs-stats', help='Gets OSRS Hi-Score data for the given user.')
    async def getOSRSStats(self, ctx, *args):

        parameters = " ".join(args[:]).split(",")
        usernames = []
        for parameter in parameters:
            usernames.append(parameter.strip())

        if not usernames[0]:
            await ctx.send(f"This command requires parameters. See correct usages below.\n`!osrs-stats Zezima` or `!osrs-stats Zezima, Lynx Titan`")
            raise Exception("User passed no parameters")

        if len(usernames) > 2:
            await ctx.send("This command currently only accepts two parameters.")
            raise Exception("User tried to use more than two parameters")

        for username in usernames:
            if getOSRS(username) == False:
                await ctx.send(f"Could not find {username} in the Hi-Scores")
                raise Exception("User searched for invalid username")


        def getOutput(username):
            skills = getOSRS(username)

            if skills:
                output = ""
                for skill_name, skill_info in skills.items():
                    level = skill_info["Level"]
                    rank = skill_info["Rank"]
                    experience = skill_info["Experience"]
                    experience = f"{int(experience):,d}"
                    output += f"\n**{skill_name}**: {level} [{experience} XP]"
                embed.add_field(name=f"{username}", value=output, inline=True)

        if len(usernames) == 1:
            embed = discord.Embed(title=f"Stats for {usernames[0]}", description="Stats fetched from OSRS Hi-Scores.", color=0xC0A886)
            getOutput(usernames[0])

        if len(usernames) == 2:
            embed = discord.Embed(title=f"Stats for {usernames[0]} and {usernames[1]}", description="Stats fetched from OSRS Hi-Scores.", color=0xC0A886)
            getOutput(usernames[0])
            getOutput(usernames[1])

        embed.set_thumbnail(url="https://lh3.googleusercontent.com/5Dj_vzUhLURKE7dnDElvo9lbgzaMynzT0tyyvStQUt3pSZ8Ub0jzsa05oVy4EtHjEq8=s180-rw")
        await ctx.send(embed=embed)



def getOSRS(username):
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
        return skills
    else:
        return False


def getItemID(searchTerm):
    import requests
    import json

    resp = requests.get('https://www.osrsbox.com/osrsbox-db/items-summary.json')

    if resp.ok:
        result = resp.json()

        for item in result.values():
            if item["name"].lower() == searchTerm.lower():
                return item["id"]

    return False



def setup(bot):
    bot.add_cog(OSRS(bot))
