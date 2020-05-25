import discord
from discord.ext import commands

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='github', help='Returns a link to the GitHub repository for this bot.')
    async def getGithubLink(self, ctx):
        await ctx.send('The GitHub link for this project is:\nhttps://github.com/jamiewhittaker/PurpBot')

def setup(bot):
    bot.add_cog(misc(bot))
