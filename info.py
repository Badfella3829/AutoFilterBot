import re
import time
import sys
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


def get_env(key, default=None, required=False):
    """Get environment variable with optional default and required check."""
    value = environ.get(key)
    if value is None:
        if required:
            print(f"ERROR: Required environment variable '{key}' is not set!")
            sys.exit(1)
        return default
    return value


# PyroClient Setup (Required)
try:
    API_ID = int(get_env('API_ID', required=True))
except ValueError:
    print("ERROR: API_ID must be a valid integer!")
    sys.exit(1)

API_HASH = get_env('API_HASH', required=True)
BOT_TOKEN = get_env('BOT_TOKEN', required=True)

# Bot settings
WEB_SUPPORT = is_enabled(get_env("WEBHOOK", 'True'), True)
PICS = get_env('PICS', 'https://telegra.ph/file/216c233c62bfeb241b359.jpg https://telegra.ph/file/f7a0e18e59b404d69ee3d.jpg https://telegra.ph/file/1a2b6e76af675065491a7.jpg https://te.legra.ph/file/142cfa1f05626acf24241.jpg').split()
UPTIME = time.time()

# Admins, Channels & Users
CACHE_TIME = int(get_env('CACHE_TIME', '300'))
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in get_env('ADMINS', '').split() if admin]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in get_env('CHANNELS', '0').split() if ch]
auth_users = [int(user) if id_pattern.search(user) else user for user in get_env('AUTH_USERS', '').split() if user]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = get_env('AUTH_CHANNEL')
auth_grp = get_env('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split() if ch] if auth_grp else None

# MongoDB information
DATABASE_URL = get_env('DATABASE_URL', "")
if not DATABASE_URL:
    print("WARNING: DATABASE_URL is not set! Database features will not work.")
DATABASE_NAME = get_env('DATABASE_NAME', "Cluster0")
FILE_DB_URL = get_env("FILE_DB_URL", DATABASE_URL)
FILE_DB_NAME = get_env("FILE_DB_NAME", DATABASE_NAME)
COLLECTION_NAME = get_env('COLLECTION_NAME', 'Telegram_files')

# Filters Configuration 
MAX_RIST_BTNS = int(get_env('MAX_RIST_BTNS', "10"))
START_MESSAGE = get_env('START_MESSAGE', script.START_TXT)
BUTTON_LOCK_TEXT = get_env("BUTTON_LOCK_TEXT", script.BUTTON_LOCK_TEXT)
FORCE_SUB_TEXT = get_env('FORCE_SUB_TEXT', script.FORCE_SUB_TEXT)

WELCOM_PIC = get_env("WELCOM_PIC", "https://telegra.ph/file/216c233c62bfeb241b359.jpg https://telegra.ph/file/f7a0e18e59b404d69ee3d.jpg https://telegra.ph/file/1a2b6e76af675065491a7.jpg https://te.legra.ph/file/142cfa1f05626acf24241.jpg")
WELCOM_TEXT = get_env("WELCOM_TEXT", script.WELCOM_TEXT)
PMFILTER = is_enabled(get_env('PMFILTER', "True"), True)
G_FILTER = is_enabled(get_env("G_FILTER", "True"), True)
BUTTON_LOCK = is_enabled(get_env("BUTTON_LOCK", "True"), True)
RemoveBG_API = get_env("RemoveBG_API", "")

# URL shortener
SHORT_URL = get_env("SHORT_URL")
SHORT_API = get_env("SHORT_API")

# Others
IMDB_DELET_TIME = int(get_env('IMDB_DELET_TIME', "300"))
LOG_CHANNEL = int(get_env('LOG_CHANNEL', '0'))
SUPPORT_CHAT = get_env('SUPPORT_CHAT', 'DevilServers')
P_TTI_SHOW_OFF = is_enabled(get_env('P_TTI_SHOW_OFF', "True"), True)
PM_IMDB = is_enabled(get_env('PM_IMDB', "True"), True)
IMDB = is_enabled(get_env('IMDB', "True"), True)
SINGLE_BUTTON = is_enabled(get_env('SINGLE_BUTTON', "True"), True)
CUSTOM_FILE_CAPTION = get_env("CUSTOM_FILE_CAPTION", "{file_name}")
BATCH_FILE_CAPTION = get_env("BATCH_FILE_CAPTION", None)
IMDB_TEMPLATE = get_env("IMDB_TEMPLATE", script.IMDB_TEMPLATE)
LONG_IMDB_DESCRIPTION = is_enabled(get_env("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(get_env("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = get_env("MAX_LIST_ELM", None)
FILE_STORE_CHANNEL = [int(ch) for ch in get_env('FILE_STORE_CHANNEL', '').split() if ch]
MELCOW_NEW_USERS = is_enabled(get_env('MELCOW_NEW_USERS', "True"), True)
PROTECT_CONTENT = is_enabled(get_env('PROTECT_CONTENT', "False"), False)
PUBLIC_FILE_STORE = is_enabled(get_env('PUBLIC_FILE_STORE', "True"), True)
LOG_MSG = "{} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ....\n\nDᴀᴛᴇ : {}\nTɪᴍᴇ : {}\n\nRᴇᴏᴩ: {}\nVᴇʀsɪᴏɴ: {}\nLɪᴄᴇɴꜱᴇ: {}\nCᴏᴩʏʀɪɢʜᴛ: {}"
