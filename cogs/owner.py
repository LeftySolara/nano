import discord
from discord.ext import commands


class Owner:
    """A cog containing owner-restricted commands"""

    def __init__(self, bot):
        self.bot = bot

    # TODO: Add a check for the user running the command
    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Log out and shut down Nano"""
        self.bot.logger.info(
            "Received shutdown signal. Closing connections...")
        await ctx.send("Goodbye :wave:")
        await self.bot.logout()

    @commands.command(name="contact")
    @commands.is_owner()
    async def contact(self, ctx):
        """Send a message to the bot's owner"""
        author = ctx.author
        colour = author.colour
        message = self.bot.clean_message(ctx)
        guild = ctx.message.guild.name

        embed = discord.Embed(
            title="Sent by {} from {}".format(author.display_name, guild),
            description=message,
            colour=colour)
        embed.set_thumbnail(url=author.avatar_url)

        owner = self.bot.get_user(self.bot.owner_id)
        await owner.send(embed=embed)
        await ctx.send("Your message has been sent.")


def setup(bot):
    bot.add_cog(Owner(bot))
