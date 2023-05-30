import logging
import os
import sys
import time

from pyrogram import Client, errors
from pyrogram.types import Message
from pyrogram.types import Chat, User
from config import Config


StartTime = time.time()

#logging
FORMAT = "[GodOfDeath] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
LOGGER = logging.getLogger(__name__)

#config
API_ID = Config.API_ID
API_HASH = Config.API_HASH
OWNER_ID = Config.OWNER_ID
OWNER_USERNAME = Config.OWNER_USERNAME
BOT_ID = Config.BOT_ID
BOT_USERNAME = Config.BOT_USERNAME
BOT_TOKEN = Config.BOT_TOKEN
START_IMG = Config.START_IMG
SUPPORT = Config.SUPPORT
UPDATES = Config.UPDATES

try:
    INFINITY_GODS = set(int(x) for x in Config.INFINITY_GODS or [])
    ULTIMATE_GODS = set(int(x) for x in Config.ULTIMATE_GODS or [])
    SUPERIORS = set(int(x) for x in Config.SUPERIOR or [])
    LEGENDS = set(int(x) for x in Config.LEGENDS or [])
    MEN = set(int(x) for x in Config.MEN or [])
    VIRUS = set(int(x) for x in Config.VIRUS or [])
except ValueError:
    raise Exception('The config value for a gods or virus is not a valid integer, Please check.')

INFINITY_GODS.append(OWNER_ID)
ULTIMATE_GODS.append(OWNER_ID)

INFINITY_GODS = list(INFINITY_GODS)
ULTIMATE_GODS = list(ULTIMATE_GODS)
SUPERIORS = list(SUPERIORS)
LEGENDS = list(LEGENDS)
MEN = list(MEN)
VIRUS = list(VIRUS)

#bot
app = Client('godofdeath', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)