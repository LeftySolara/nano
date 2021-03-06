import sys
import traceback
import time
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


class Nano(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.config = Config()
        self.command_prefix = self.config.get_prefix()
        self.logger = self.logging_init()
        self.start_time = time.time()
        self.core_extensions = ["cogs.basic", "cogs.owner"]

        kwargs["description"] = self.config.get_description()
        kwargs["pm_help"] = True

        super().__init__(*args, command_prefix=self.command_prefix, **kwargs)

        for extention in self.core_extensions:
            try:
                self.load_extension(extention)
            except Exception as e:
                self.logger.error(
                    "Failed to load extension {}".format(extention))
                traceback.print_exc()

    def logging_init(self):
        name = self.config.get_name().lower()
        filename = self.config.get_logname()
        level = self.config.get_loglevel()

        logger = logging.getLogger(name.lower())
        logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        logHandler = logging.handlers.RotatingFileHandler(
            filename, maxBytes=10 * 1024 * 1024, backupCount=5)
        logHandler.setLevel(level)
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)

        return logger

    def clean_message(self, ctx: commands.Context):
        """Return a message with the command prefix and name removed."""
        content = ctx.message.content
        prefix = ctx.prefix
        command = ctx.command.name

        return content.replace(prefix + command, '')



nano = Nano()


@nano.event
async def on_ready():
    print("Logged in as {}".format(nano.user.name))
    print("User ID: {}".format(nano.user.id))
    print("--------")
    nano.logger.info("Successfully logged in as {} with user id {}.".format(
        nano.user.name, nano.user.id))


nano.run(nano.config.get_token())
