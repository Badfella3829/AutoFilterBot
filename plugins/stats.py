"""
Stats and monitoring commands for the AutoFilterBot.
"""

import os
import time
import logging
import psutil
from datetime import datetime

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from info import ADMINS, LOG_CHANNEL
from database.users_chats_db import db
from database.ia_filterdb import Media

logger = logging.getLogger(__name__)

START_TIME = datetime.now()


def format_bytes(size):
    """Format bytes to human readable string."""
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024.0 and i < len(units) - 1:
        i += 1
        size /= 1024.0
    return f"{size:.2f} {units[i]}"


def get_uptime():
    """Get bot uptime as string."""
    delta = datetime.now() - START_TIME
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    return f"{hours}h {minutes}m {seconds}s"


@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats_command(client, message):
    """Show comprehensive bot statistics."""
    sts = await message.reply("Fetching statistics...")

    try:
        total_users = await db.total_users_count()
        total_chats = await db.total_chat_count()
        total_files = await Media.count_documents({})

        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        stats_text = f"""<b>Bot Statistics</b>

<b>Database Stats:</b>
- Total Users: <code>{total_users:,}</code>
- Total Chats: <code>{total_chats:,}</code>
- Total Files: <code>{total_files:,}</code>

<b>System Stats:</b>
- CPU Usage: <code>{cpu}%</code>
- RAM Usage: <code>{mem.percent}%</code>
- RAM Used: <code>{format_bytes(mem.used)}</code>
- Disk Usage: <code>{disk.percent}%</code>
- Disk Used: <code>{format_bytes(disk.used)}</code>

<b>Bot Info:</b>
- Uptime: <code>{get_uptime()}</code>
- Started: <code>{START_TIME.strftime('%Y-%m-%d %H:%M:%S')}</code>
"""

        buttons = [[
            InlineKeyboardButton("Refresh", callback_data="refresh_stats"),
            InlineKeyboardButton("Close", callback_data="close_data")
        ]]

        await sts.edit(stats_text, reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        logger.exception(f"Error fetching stats: {e}")
        await sts.edit(f"Error fetching statistics: {e}")


@Client.on_callback_query(filters.regex("^refresh_stats$") & filters.user(ADMINS))
async def refresh_stats_callback(client, query):
    """Refresh the stats display."""
    try:
        total_users = await db.total_users_count()
        total_chats = await db.total_chat_count()
        total_files = await Media.count_documents({})

        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        stats_text = f"""<b>Bot Statistics</b>

<b>Database Stats:</b>
- Total Users: <code>{total_users:,}</code>
- Total Chats: <code>{total_chats:,}</code>
- Total Files: <code>{total_files:,}</code>

<b>System Stats:</b>
- CPU Usage: <code>{cpu}%</code>
- RAM Usage: <code>{mem.percent}%</code>
- RAM Used: <code>{format_bytes(mem.used)}</code>
- Disk Usage: <code>{disk.percent}%</code>
- Disk Used: <code>{format_bytes(disk.used)}</code>

<b>Bot Info:</b>
- Uptime: <code>{get_uptime()}</code>
- Last Updated: <code>{datetime.now().strftime('%H:%M:%S')}</code>
"""

        buttons = [[
            InlineKeyboardButton("Refresh", callback_data="refresh_stats"),
            InlineKeyboardButton("Close", callback_data="close_data")
        ]]

        await query.message.edit(stats_text, reply_markup=InlineKeyboardMarkup(buttons))
        await query.answer("Stats refreshed!")

    except Exception as e:
        logger.exception(f"Error refreshing stats: {e}")
        await query.answer(f"Error: {e}", show_alert=True)


@Client.on_message(filters.command("ping") & filters.user(ADMINS))
async def ping_command(client, message):
    """Check bot latency."""
    start = time.time()
    msg = await message.reply("Pong!")
    end = time.time()
    latency = (end - start) * 1000
    await msg.edit(f"Pong! Latency: <code>{latency:.2f}ms</code>")
