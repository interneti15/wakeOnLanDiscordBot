import os

from dotenv import load_dotenv

class Config:
    """Configuration class."""
    def __init__(self):
        load_dotenv()
        self.DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
        self.SPECIFIED_USER_ID = int(os.environ.get("SPECIFIED_USER_ID","0"))
        self.MAC_ADDRESS = os.environ.get("MAC_ADDRESS")