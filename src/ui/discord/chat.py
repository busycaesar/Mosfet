import asyncio
import discord
from core import parse_user_input
from config import DISCORD_MESSAGE_LIMIT
from .client import client
from .interaction import confirm_tool_call
from .activity_log import DiscordActivityLog

activity_log = DiscordActivityLog()

async def send_long_message(channel, text):
    """
    Discord throws error for messages beyond 2000 characters.
    Hence breaking the long messages beyond 2000 characters into multiple messages.
    """
    for i in range(0, len(text), DISCORD_MESSAGE_LIMIT):
        await channel.send(text[i:i + DISCORD_MESSAGE_LIMIT])

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

@client.event
async def on_message(message):
    # Ensure that it does not reply to itself.
    if message.author == client.user:
        return

    # Ensure only direct messages are allowed.
    if not isinstance(message.channel, discord.DMChannel):
        return

    def confirm_tool_call_in_channel(function_name):
        return confirm_tool_call(message.channel, function_name)

    conversation = client.conversation
    start_index = len(conversation.messages)

    async with message.channel.typing():
        try:
            response = await asyncio.to_thread(
                parse_user_input, 
                conversation.messages, 
                message.content, 
                confirm_tool_call_in_channel, 
                activity_log
            )
        except Exception as error:
            await message.channel.send(f"Error: {error}. Please try again.")
            return

    conversation.save_turn(start_index)

    await send_long_message(message.channel, response)
