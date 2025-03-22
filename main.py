import os
import disnake
from disnake.ext import commands
import sqlite3
from economy.economy import Economy

intents = disnake.Intents.default()
intents.message_content = True  
intents.members = True
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(command_prefix="l!", intents=intents, test_guilds=[1353007786971365407, 1349503378119462912], command_sync_flags=command_sync_flags)
bot.channel_conversations = {}
def setup_database():
    """Initialize the SQLite database for user memory."""
    bot.conn = sqlite3.connect("user_memory.db")
    bot.cursor = bot.conn.cursor()
    bot.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            info TEXT
        )
    """)
    bot.conn.commit()
bot.setup_database = setup_database

bot.setup_database()
bot.economy = Economy()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(type=disnake.ActivityType.playing, name="being devlopped", url="https://aferiad-kamal.pages.dev/"))
    files = {
        "fun": [
            "cat", "coin_flip", "dice", "greetings", "joke", "match"
        ],
        "ai": [
            "image-gen", "text-gen"
        ],
        "events": [
            "welcome"
        ],
        "economy": [
            "balance", "daily", "leaderboard", "message_listener", "gambling", "pay"
        ],
        "moderation": [
            "ban", "clear", "kick", "mute", "clone", "verify", "reactrole"
        ]
    }
    
    for folder in files:
        for file in files[folder]:
            bot.load_extension(f"{folder}.{file}")

    await bot._sync_application_commands()
        
bot.run(os.environ["TOKEN"])
