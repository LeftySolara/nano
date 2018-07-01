import sys
import logging
import logging.handlers
import discord

from discord.ext import commands
from config import Config


def logging_init(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logHandler = logging.handlers.RotatingFileHandler(
        "{}.log".format(name), maxBytes=10 * 1024 * 1024, backupCount=5)
    logHandler.setLevel(level)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger


config = Config()
logger = logging_init(config.get_name())
bot = commands.Bot(
    command_prefix=config.get_prefix(), description=config.get_description())


@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user.name))
    print("User ID: {}".format(bot.user.id))
    print("--------")
    logger.info("Successfully logged in as {} with user id {}".format(
        bot.user.name, bot.user.id))


@bot.command()
async def greet(ctx):
    """Print a nice greeting message"""
    await ctx.send(":smiley: :wave: Hello, there!")


@bot.command()
async def info(ctx):
    """Display information about the bot."""
    embed = discord.Embed(
        title=bot.user.name, description=bot.description, color=0xb294bb)

    python_version = "{}.{}.{}".format(
        sys.version_info[0], sys.version_info[1], sys.version_info[2])

    embed.add_field(name="Author", value="LeftySolara")
    embed.add_field(name="Python", value=python_version)
    embed.add_field(name="Discord.py", value=discord.__version__)

    await ctx.send(embed=embed)


bot.run(config.get_token())
