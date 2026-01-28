import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
import os

from utils.scheduler import (
    start_scheduler,
    make_scheduler_jobs,
    shutdown_scheduler,
    ps4_event,
    ps5_event,
    stored_info,
)
from utils.notification_channel_list import (
    notification_channels,
)

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()


class Snek(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        make_scheduler_jobs()

    async def setup_hook(self):
        asyncio.create_task(self.on_ps4_update())
        asyncio.create_task(self.on_ps5_update())
        start_scheduler()
        await self.load_extension("commands.notification_channel_register")
        await self.load_extension("commands.show_change_log")

    async def on_ps4_update(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await ps4_event.wait()
            for guild_id, channel_ids in notification_channels.items():
                guild = self.get_guild(int(guild_id))
                if guild:
                    for channel_id in channel_ids:
                        channel = guild.get_channel(channel_id)
                        if channel:
                            await channel.send(
                                f"New PS4 firmware update is available!\n\n## PS4 Version: {stored_info['ps4']['version']}\n{stored_info['ps4']['details']}"
                            )
            ps4_event.clear()

    async def on_ps5_update(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await ps5_event.wait()
            for guild_id, channel_ids in notification_channels.items():
                guild = self.get_guild(int(guild_id))
                if guild:
                    for channel_id in channel_ids:
                        channel = guild.get_channel(channel_id)
                        if channel:
                            await channel.send(
                                f"New PS5 firmware update is available!\n\n## PS5 Version: {stored_info['ps5']['version']}\n{stored_info['ps5']['details']}"
                            )
            ps5_event.clear()

    async def on_ready(self):
        if self.user:
            print(f"Logged in as {self.user.name} (ID: {self.user.id})")
        else:
            print("Logged in, but user is None..?")
        print("------")

    async def close(self):
        shutdown_scheduler()
        await super().close()


bot = Snek("aaaaaaaa", intents=intents)
bot.run(token)
