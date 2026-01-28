from pathlib import Path
import json


if Path("notification_channels.json").exists():
    with open("notification_channels.json", "r") as f:
        notification_channels: dict[str, list[int]] = json.load(f)
else:
    notification_channels = {}


def add_notification_channel(guild_id: int, channel_id: int) -> None:
    guild_id_str = str(guild_id)
    if guild_id_str not in notification_channels:
        notification_channels[guild_id_str] = []
    if channel_id not in notification_channels[guild_id_str]:
        notification_channels[guild_id_str].append(channel_id)
    with open("notification_channels.json", "w") as f:
        json.dump(notification_channels, f)


def remove_notification_channel(guild_id: int, channel_id: int) -> None:
    guild_id_str = str(guild_id)
    if guild_id_str in notification_channels:
        if channel_id in notification_channels[guild_id_str]:
            notification_channels[guild_id_str].remove(channel_id)
            with open("notification_channels.json", "w") as f:
                json.dump(notification_channels, f)
