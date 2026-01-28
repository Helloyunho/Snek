from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.crawler import fetch_ps4_html, fetch_ps5_html, parse_html
import json
import asyncio
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from utils.crawler import FirmwareInfo


if Path("firmware_info.json").exists():
    with open("firmware_info.json", "r") as f:
        stored_info: dict[str, "FirmwareInfo"] = json.load(f)
else:
    stored_info = {}

scheduler = AsyncIOScheduler()
ps4_event = asyncio.Event()
ps5_event = asyncio.Event()


def start_scheduler():
    scheduler.start()


async def check_for_updates():
    ps4_html = await fetch_ps4_html()
    ps5_html = await fetch_ps5_html()
    ps4_info = await parse_html(ps4_html)
    ps5_info = await parse_html(ps5_html)
    stored_ps4_version = stored_info.get("ps4", {}).get("version")
    stored_ps5_version = stored_info.get("ps5", {}).get("version")
    stored_info["ps4"] = ps4_info
    stored_info["ps5"] = ps5_info
    if stored_ps4_version != ps4_info["version"]:
        print(f"New PS4 firmware version detected: {ps4_info['version']}")
        ps4_event.set()
    if stored_ps5_version != ps5_info["version"]:
        print(f"New PS5 firmware version detected: {ps5_info['version']}")
        ps5_event.set()
    with open("firmware_info.json", "w") as f:
        json.dump(stored_info, f)


def make_scheduler_jobs():
    scheduler.add_job(check_for_updates, "interval", minutes=1)


def shutdown_scheduler():
    scheduler.shutdown()
