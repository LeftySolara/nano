import datetime
import time
import discord
from discord.ext import commands


class Owner:
    """A cog containing owner-restricted commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Log out and shut down Nano"""
        if not ctx.message.author.id == self.bot.owner_id:
            await ctx.send("Only the owner is authorized to use this command.")
        else:
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

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        now = time.time()
        timediff = int(now - self.bot.start_time)

        days = timediff // (24 * 3600)

        timediff %= (24 * 3600)
        hours = timediff // 3600

        timediff %= 3600
        minutes = timediff // 60

        timediff %= 60
        seconds = timediff

        message = "I have been up for {} days, {} hours, {} minutes, and {} seconds.".format(
            days, hours, minutes, seconds)

        await ctx.send(message)


def setup(bot):
    bot.add_cog(Owner(bot))
