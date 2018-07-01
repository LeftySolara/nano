import traceback
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
    logger.info("Successfully logged in as {} with user id {}.".format(
        bot.user.name, bot.user.id))


initial_extentions = ["cogs.basic", "cogs.owner"]

for extention in initial_extentions:
    try:
        bot.load_extension(extention)
    except Exception as e:
        logger.error("Failed to load extension {}".format(extention))
        traceback.print_exc()

bot.run(config.get_token())
