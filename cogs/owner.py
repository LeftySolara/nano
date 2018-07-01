import discord
from discord.ext import commands


class Owner:
    """A cog containing owner-restricted commands"""

    def __init__(self, bot):
        self.bot = bot

    #TODO add logging for this once the bot has its own logger
    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Log out and shut down Nano."""
        await ctx.send("Goodbye :wave:")
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Owner(bot))
