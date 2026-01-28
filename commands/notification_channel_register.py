import discord
from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING

from utils.notification_channel_list import add_notification_channel

if TYPE_CHECKING:
    from main import Snek


class NotificationChannelRegister(commands.Cog):
    def __init__(self, bot: "Snek"):
        self.bot = bot

    @app_commands.command(
        name="register",
        description="Register channel for firmware update notifications.",
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    @app_commands.describe(
        channel="The channel to register for notifications. Defaults to the current channel."
    )
    async def register(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel | None = None,
    ):
        channel = channel or interaction.channel
        assert channel is not None  # for mypy
        add_notification_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(
            f"Registered {channel.mention} for firmware update notifications.",
            ephemeral=True,
        )

    @app_commands.command(
        name="unregister",
        description="Unregister channel from firmware update notifications.",
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    @app_commands.describe(
        channel="The channel to unregister from notifications. Defaults to the current channel."
    )
    async def unregister(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel | None = None,
    ):
        channel = channel or interaction.channel
        assert channel is not None  # for mypy
        from utils.notification_channel_list import remove_notification_channel

        remove_notification_channel(interaction.guild_id, channel.id)
        await interaction.response.send_message(
            f"Unregistered {channel.mention} from firmware update notifications.",
            ephemeral=True,
        )


async def setup(bot: "Snek"):
    await bot.add_cog(NotificationChannelRegister(bot))
