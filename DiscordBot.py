import threading
import time
from datetime import datetime

from WakeOnLan import *
import discord
from CommandHandler import *

class DiscordBot:

    def __init__(self, config:Config):
        self.config = config

        intents = discord.Intents.default()
        intents.messages = True

        self.client = discord.Client(intents=intents)

        self.client_overrides()

        self.client.run(self.config.DISCORD_TOKEN)

        time.sleep(20)
        thread = threading.Thread(target=run_async_task_periodically, args=(300, send_message_to_user, config.SPECIFIED_USER_ID, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.client))
        thread.daemon = True  # Ensures the thread exits when the main program ends
        thread.start()

    def client_overrides(self):
        @self.client.event
        async def on_ready():
            """Event that triggers when the bot has successfully connected."""
            print(f'Logged in as {self.client.user}')

            # Send a message to a specific user
            await send_message_to_user(self.config.SPECIFIED_USER_ID, "Started.", self.client)

            # Change bot presence (Only status set to online)
            await self.client.change_presence(
                status=discord.Status.do_not_disturb
            )

        @self.client.event
        async def on_message(message: discord.Message):
            print(message.author.name, message.content)
            """Event triggered when a new message is received."""
            # Check if the message is a DM and the sender is the specified user
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
        user = await client.fetch_user(user_id)  # Fetch the user by ID
        await user.send(message_content)  # Send the message
        print(f"Message sent to {user.name}: {message_content}")
    except discord.HTTPException as e:
        print(f"Failed to send message: {e}")
    except discord.NotFound:
        print("User not found.")
    except discord.Forbidden:
        print("Cannot send messages to this user (bot lacks permissions).")

def run_async_task_periodically(interval, coro, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        loop.run_until_complete(coro(*args))
        time.sleep(interval)