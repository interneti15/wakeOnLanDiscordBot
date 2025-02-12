import asyncio
import time
from datetime import datetime
import discord

from WakeOnLan import *
from CommandHandler import *
from Config import *

class DiscordBot:

    def __init__(self, config:Config):
        self.config = config

        intents = discord.Intents.default()
        intents.messages = True

        self.client = discord.Client(intents=intents)

        self.client_overrides()

        self.client.run(self.config.DISCORD_TOKEN)

    def client_overrides(self):
        @self.client.event
        async def on_ready():
            """Event that triggers when the bot has successfully connected."""
            print(f'Logged in as {self.client.user}')

            await send_message_to_user(self.config.SPECIFIED_USER_ID, "Started.", self.client)

            await self.client.change_presence(
                status=discord.Status.do_not_disturb
            )

            self.client.loop.create_task(run_async_task_periodically(300, self.client, self.config))

        @self.client.event
        async def on_message(message: discord.Message):
            """Event triggered when a new message is received."""
            if isinstance(message.channel, discord.DMChannel) and message.author.id == self.config.SPECIFIED_USER_ID:
                return_message = await commandHandler(message.content, self.config)
                await send_message_to_user(self.config.SPECIFIED_USER_ID, return_message, self.client)

async def send_message_to_user(user_id, message_content, client):
    """
    Sends a direct message to a user with the specified user ID.

    Args:
        user_id (int): The Discord user ID to message.
        message_content (str): The content of the message to send.
        client (discord.Client): The active Discord client.
    """
    try:
        user = await client.fetch_user(user_id)
        await user.send(message_content)
        print(f"Message sent to {user.name}: {message_content}")
    except discord.HTTPException as e:
        print(f"Failed to send message: {e}")
    except discord.NotFound:
        print("User not found.")
    except discord.Forbidden:
        print("Cannot send messages to this user (bot lacks permissions).")

async def run_async_task_periodically(interval, client, config:Config):
    print(1)
    await asyncio.sleep(7)
    print(2)
    while True:
        await send_message_to_user(config.SPECIFIED_USER_ID, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), client)
        await asyncio.sleep(interval)
