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
                    birthdays.append(villager["name"]["name-USen"])

            formattedDate = now.strftime("%d/%m/%Y")
            output = f"The following villagers have birthdays today: ({formattedDate})\n```"
            for name in birthdays:
                output = f"{output}* {name}\n"

            output = output + "```"
            await ctx.send(output)


def setup(bot):
    bot.add_cog(AC(bot))
