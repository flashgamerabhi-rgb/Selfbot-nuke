"""
Configuration file for Discord Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', 0))
PREFIX = '.'
BOT_NAME = "ALPHA SELFBOT"

# Validation
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")
if OWNER_ID == 0:
    raise ValueError("OWNER_ID not found in .env file")
