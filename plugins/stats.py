"""
Stats and monitoring commands for the AutoFilterBot.

Provides admin commands for monitoring bot statistics,
database status, and system resources.
"""

import logging
import asyncio
from datetime import datetime

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from info import ADMINS, LOG_CHANNEL
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils.health import health_checker, format_bytes

logger = logging.getLogger(__name__)


@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats_command(client, message):
    """Show comprehensive bot statistics."""
    sts = await message.reply("Fetching statistics...")
    
    try:
        # Get database stats
        total_users = await db.total_users_count()
        total_chats = await db.total_chat_count()
        total_files = await Media.count_documents({})
        
        # Get system stats
        system_stats = health_checker.get_system_stats()
        
        # Format the stats message
        stats_text = f"""<b>Bot Statistics</b>

<b>Database Stats:</b>
- Total Users: <code>{total_users:,}</code>
- Total Chats: <code>{total_chats:,}</code>
- Total Files: <code>{total_files:,}</code>

<b>System Stats:</b>
- CPU Usage: <code>{system_stats['cpu_percent']}%</code>
- RAM Usage: <code>{system_stats['memory']['percent']}%</code>
- RAM Used: <code>{format_bytes(system_stats['memory']['used'])}</code>
- Disk Usage: <code>{system_stats['disk']['percent']}%</code>
- Disk Used: <code>{format_bytes(system_stats['disk']['used'])}</code>

<b>Bot Info:</b>
- Uptime: <code>{health_checker.uptime_str}</code>
- Started: <code>{health_checker.start_time.strftime('%Y-%m-%d %H:%M:%S')}</code>
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
        # Get database stats
        total_users = await db.total_users_count()
        total_chats = await db.total_chat_count()
        total_files = await Media.count_documents({})
        
        # Get system stats
        system_stats = health_checker.get_system_stats()
        
        stats_text = f"""<b>Bot Statistics</b>

<b>Database Stats:</b>
- Total Users: <code>{total_users:,}</code>
- Total Chats: <code>{total_chats:,}</code>
- Total Files: <code>{total_files:,}</code>

<b>System Stats:</b>
- CPU Usage: <code>{system_stats['cpu_percent']}%</code>
- RAM Usage: <code>{system_stats['memory']['percent']}%</code>
- RAM Used: <code>{format_bytes(system_stats['memory']['used'])}</code>
- Disk Usage: <code>{system_stats['disk']['percent']}%</code>
- Disk Used: <code>{format_bytes(system_stats['disk']['used'])}</code>

<b>Bot Info:</b>
- Uptime: <code>{health_checker.uptime_str}</code>
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


@Client.on_message(filters.command("dbstats") & filters.user(ADMINS))
async def db_stats_command(client, message):
    """Show detailed database statistics."""
    sts = await message.reply("Fetching database statistics...")
    
    try:
        total_users = await db.total_users_count()
        total_chats = await db.total_chat_count()
        total_files = await Media.count_documents({})
        
        # Get collection sizes (approximate)
        db_stats_text = f"""<b>Database Statistics</b>

<b>Collections:</b>
- Users Collection: <code>{total_users:,}</code> documents
- Chats Collection: <code>{total_chats:,}</code> documents  
- Files Collection: <code>{total_files:,}</code> documents

<b>Storage Info:</b>
- Estimated Total Documents: <code>{total_users + total_chats + total_files:,}</code>
"""
        
        await sts.edit(db_stats_text)
        
    except Exception as e:
        logger.exception(f"Error fetching db stats: {e}")
        await sts.edit(f"Error fetching database statistics: {e}")


@Client.on_message(filters.command("ping") & filters.user(ADMINS))
async def ping_command(client, message):
    """Check bot latency."""
    import time
    start = time.time()
    msg = await message.reply("Pong!")
    end = time.time()
    
    latency = (end - start) * 1000
    await msg.edit(f"Pong! Latency: <code>{latency:.2f}ms</code>")


@Client.on_message(filters.command("logs") & filters.user(ADMINS))
async def logs_command(client, message):
    """Send recent log file to admin."""
    try:
        # Try to read the log file
        log_file = "bot.log"
        try:
            with open(log_file, 'r') as f:
                # Get last 50 lines
                lines = f.readlines()[-50:]
                log_content = ''.join(lines)
        except FileNotFoundError:
            return await message.reply("No log file found. Logging might be configured differently.")
        
        if len(log_content) > 4000:
            # Send as file
            await message.reply_document(
                document=log_file,
                caption="Recent bot logs"
            )
        else:
            await message.reply(f"<b>Recent Logs:</b>\n<code>{log_content}</code>")
            
    except Exception as e:
        logger.exception(f"Error fetching logs: {e}")
        await message.reply(f"Error fetching logs: {e}")
