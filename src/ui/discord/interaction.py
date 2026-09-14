import asyncio
import discord
from .client import client

CONFIRM_TIMEOUT_SECONDS = 300

class ConfirmView(discord.ui.View):
    """
    Yes/No buttons for a tool-permission request. Defaults to denied if nobody clicks within CONFIRM_TIMEOUT_SECONDS.
    """

    def __init__(self):
        super().__init__(timeout=CONFIRM_TIMEOUT_SECONDS)
        self.result = None

    @discord.ui.button(label="Allow", style=discord.ButtonStyle.success)
    async def allow(self, interaction, button):
        self.result = True
        await interaction.response.send_message("Allowed.", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger)
    async def deny(self, interaction, button):
        self.result = False
        await interaction.response.send_message("Denied.", ephemeral=True)
        self.stop()

async def ask_discord_confirmation(channel, function_name, function_arguments):
    view = ConfirmView()

    await channel.send(f"Allow tool call `{function_name}({function_arguments})`?", view=view)

    await view.wait()

    return view.result if view.result is not None else False

def confirm_tool_call(channel, function_name, function_arguments):
    future = asyncio.run_coroutine_threadsafe(
        ask_discord_confirmation(channel, function_name, function_arguments),
        client.loop,
    )
    return future.result()
