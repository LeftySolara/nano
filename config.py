import configparser
import pathlib

# Default settings for the bot. These are written in INI style, with a dict
# to hold the values. This dict is formatted {"Section": {"Setting": "Value"}}.
DEFAULT_CONFIG = {
    "BOT": {
        "name": "Nano",
        "prefix": '!',
        "description": "Not a robot!"
    },
    "LOG": {
        "filename": "nano.log"
    }
}


class Config:
    """Class for parsing and managing settings for the bot."""

    def __init__(self, config_file="config"):
        self.config = configparser.ConfigParser()
        self.file_path = pathlib.Path(config_file)
        self.defaults = DEFAULT_CONFIG
        self.first_run = not self.file_path.exists()

        if self.first_run:
            self.apply_defaults()
            self.setup_interactive()
        else:
            self.config.read(self.file_path)

    def write(self):
        """Write cached settings to the config file."""
        with open(self.file_path, 'w') as config_file:
            self.config.write(config_file)

    def apply_defaults(self, write=False):
        """Apply default settings to the current instance of the bot."""
        self.config.read_dict(self.defaults)
        if write:
            self.write()

    def setup_interactive(self):
        """Interactive setup for first run."""
        token = input("Please enter your bot user's token: ")
        prefix = input("Enter a prefix for your bot (default is '!'): ")

        if not self.config.has_section("BOT"):
            self.config.add_section("BOT")

        if prefix == '':
            prefix = DEFAULT_CONFIG["BOT"]["prefix"]

        self.config.set("BOT", "token", token)
        self.config.set("BOT", "prefix", prefix)

        self.write()

    def get_token(self):
        return self.config.get("BOT", "token")

    def get_name(self):
        return self.config.get("BOT", "name")

    def get_prefix(self):
        return self.config.get("BOT", "prefix")

    def get_description(self):
        return self.config.get("BOT", "description")
