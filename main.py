"""
ALPHA SELFBOT - Discord Bot
A high-performance selfbot with nuke, spam, and mass commands
Owner only - All commands visible only to owner
"""
import discord
from discord.ext import commands
import asyncio
from config import DISCORD_TOKEN, OWNER_ID, PREFIX, BOT_NAME
import sys

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None,
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="https://discord.gg/6s5ZSV4ZcB"
    )
)

# Store for cogs
COGS = [
    'cogs.nuke',
    'cogs.spam',
    'cogs.utility'
]

async def load_cogs():
    """Load all cogs"""
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✓ Loaded {cog}")
        except Exception as e:
            print(f"✗ Failed to load {cog}: {e}")

@bot.event
async def on_ready():
    """Bot ready event"""
    print("\n" + "="*60)
    print(f"╔════════════════════════════════════════════════════════╗")
    print(f"║                                                        ║")
    print(f"║          🚀 ALPHA SELFBOT - ONLINE 🚀                 ║")
    print(f"║                                                        ║")
    print(f"║  Owner: {str(OWNER_ID):<46} ║")
    print(f"║  Prefix: {PREFIX:<45} ║")
    print(f"║  Status: READY                                         ║")
    print(f"║  Invite: https://discord.gg/6s5ZSV4ZcB                ║")
    print(f"║                                                        ║")
    print(f"╚════════════════════════════════════════════════════════╝")
    print("="*60 + "\n")
    
    # Set bot bio/status
    try:
        await bot.user.edit(bio="🔗 https://discord.gg/6s5ZSV4ZcB")
    except:
        pass

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.NotOwner):
        # Only show error to owner
        if ctx.author.id == OWNER_ID:
            await ctx.send("❌ Owner only command")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        print(f"Error: {error}")

async def main():
    """Main function"""
    async with bot:
        await load_cogs()
        try:
            await bot.start(DISCORD_TOKEN)
        except discord.LoginFailure:
            print("❌ Invalid token. Check your .env file.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✓ Bot stopped.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
