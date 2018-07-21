import time
import traceback
import discord
from discord.ext import commands


class Owner:
    """A cog containing owner-restricted commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Logs out and shuts down Nano"""
        self.bot.logger.info(
            "Received shutdown signal. Closing connections...")
        await ctx.send("Goodbye :wave:")
        await self.bot.logout()

    @commands.command(name="contact")
    async def contact(self, ctx):
        """Sends a message to the owner"""
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

    @commands.command(name="load")
    @commands.is_owner()
    async def load(self, ctx):
        """Loads a cog"""
        cog_name = self.bot.clean_message(ctx).strip()
        if self.bot.get_cog(cog_name.capitalize()):
            await ctx.send("Cog \"{}\" already loaded.".format(cog_name))
            return

        try:
            self.bot.load_extension("cogs." + cog_name)
            await ctx.send("Loaded cog \"{}\".".format(cog_name))
            self.bot.logger.info(
                "Command Load: loaded extension {}".format(cog_name))
        except Exception as e:
            await ctx.send("Error: unable to load cog.")
            self.bot.logger.error(
                "Command Load: Failed to load extension {}".format(cog_name))
            traceback.print_exc()

    @commands.command(name="unload")
    @commands.is_owner()
    async def unload(self, ctx):
        """Unloads a cog"""
        cog_name = self.bot.clean_message(ctx).strip()
        if "cogs.{}".format(cog_name) in self.bot.core_extensions:
            await ctx.send("Cannot unload core cog.")
            return

        if self.bot.get_cog(cog_name.capitalize()):
            self.bot.unload_extension("cogs." + cog_name)
            await ctx.send("Unloaded cog {}.".format(cog_name))
            self.bot.logger.info("Command Unload: unloaded extension {}".
                                 format(cog_name.capitalize()))
        else:
            await ctx.send("Cog \"{}\" not found.".format(cog_name))

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        """Shows Nano's uptime"""
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
