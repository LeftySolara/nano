import sys
import traceback
import logging
import logging.handlers

try:
    import discord
    from discord.ext import commands
except ModuleNotFoundError:
    print("discord.py is not installed.\n"
          "Instructions for installation can be found at "
          "https://discordpy.readthedocs.io/en/rewrite/")
    sys.exit(1)

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


class Nano(commands.Bot):
    config = Config()
    logger = logging_init(config.get_name())

    def __init__(self):
        self.command_prefix = self.config.get_prefix()
        self.description = self.config.get_description()

        super().__init__(
            command_prefix=self.command_prefix, description=self.description)


nano = Nano()


@nano.event
async def on_ready():
    print("Logged in as {}".format(nano.user.name))
    print("User ID: {}".format(nano.user.id))
    print("--------")
    nano.logger.info("Successfully logged in as {} with user id {}.".format(
        nano.user.name, nano.user.id))


initial_extentions = ["cogs.basic", "cogs.owner"]

for extention in initial_extentions:
    try:
        nano.load_extension(extention)
    except Exception as e:
        nano.logger.error("Failed to load extension {}".format(extention))
        traceback.print_exc()

nano.run(nano.config.get_token())
