import sys
import discord
from discord.ext import commands


class Basic:
    """A cog containing basic bot commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="greet", aliases=["hello"])
    async def greet(self, ctx):
        """Prints a nice greeting message"""
        await ctx.send(":smiley: :wave: Hello, there!")

    @commands.command(name="info", aliases=["information"])
    async def info(self, ctx):
        """Displays information about Nano"""
        embed = discord.Embed(
            title=self.bot.user.name,
            description=self.bot.description,
            color=0xb294bb)

        python_version = "{}.{}.{}".format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2])

        embed.add_field(name="Author", value="LeftySolara")
        embed.add_field(name="Python", value=python_version)
        embed.add_field(name="Discord.py", value=discord.__version__)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Basic(bot))
