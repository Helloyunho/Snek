import discord
from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING

from utils.scheduler import stored_info

if TYPE_CHECKING:
    from main import Snek


class ShowChangeLog(commands.Cog):
    def __init__(self, bot: "Snek"):
        self.bot = bot

    @app_commands.command(
        name="ps4",
        description="Show the latest PS4 firmware update changelog.",
    )
    async def ps4(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            f"## PS4 Version: {stored_info['ps4']['version']}\n{stored_info['ps4']['details']}",
            ephemeral=True,
        )

    @app_commands.command(
        name="ps5",
        description="Show the latest PS5 firmware update changelog.",
    )
    async def ps5(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.send_message(
            f"## PS5 Version: {stored_info['ps5']['version']}\n{stored_info['ps5']['details']}",
            ephemeral=True,
        )


async def setup(bot: "Snek"):
    await bot.add_cog(ShowChangeLog(bot))
