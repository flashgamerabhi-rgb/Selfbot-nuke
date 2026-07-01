# 🚀 ALPHA SELFBOT - NUKE & SPAM

High-performance Discord bot with lightning-fast nuke, spam, and mass channel commands.

## ⚡ FEATURES

✅ **MAXIMUM SPEED** - All commands run at lightning speed  
✅ **NO DELAYS** - No latency, no timeout  
✅ **MASS OPERATIONS** - Nuke, create, spam in seconds  
✅ **OWNER ONLY** - Secure commands  
✅ **10X SPAM** - Spam each channel 10 times instantly  
✅ **ASYNC OPERATIONS** - All tasks run simultaneously  

## 📋 COMMANDS

### NUKE COMMANDS
```
.nuke                          Delete ALL channels instantly
.deletechannels                Delete all channels (alias)
.createchannels <count> <name> Create multiple channels
.create <count> <name>         Quick create alias
.multicreate <count> <name>    Fast multi-channel creation
```

### SPAM COMMANDS
```
.spam <count> <#channel> <msg> Spam message in specific channel
.spamall <count> <message>     Spam message in ALL channels
.multispam <message>           Spam ALL channels 10x each (NO DELAY)
```

### UTILITY COMMANDS
```
.help                          Show all commands
.owner                         Get owner info
.serverinfo                    Get server information
.ping                          Check bot latency
.stats                         Show bot statistics
.test                          Test bot connection
```

## 🚀 SETUP

### 1. Get Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create "New Application"
3. Go to "Bot" → "Add Bot"
4. Copy the token
5. Enable these intents:
   - Message Content Intent ✓
   - Server Members Intent ✓
   - Guild Members Intent ✓

### 2. Get Your Discord ID
1. Enable Developer Mode in Discord Settings
2. Right-click your profile → Copy User ID

### 3. Install Bot in Server
1. Go to OAuth2 → URL Generator
2. Select scopes: `bot`
3. Select permissions: `Administrator`
4. Copy and open the generated URL

### 4. Setup Project

```bash
# Clone repository
git clone https://github.com/flashgamerabhi-rgb/Selfbot-nuke.git
cd Selfbot-nuke

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your values
echo "DISCORD_TOKEN=your_token_here" > .env
echo "OWNER_ID=your_id_here" >> .env
```

### 5. Run Bot

```bash
python main.py
```

## 🎯 EXAMPLE USAGE

### Create 50 channels named "spam"
```
.createchannels 50 spam
```

### Spam "Hello" 100 times in #general
```
.spam 100 #general Hello
```

### Spam "NUKED" in ALL channels, 10 times each
```
.multispam NUKED
```

### Delete ALL channels (with confirmation)
```
.nuke
```

## ⚙️ HOW IT WORKS

### MAXIMUM SPEED TECHNOLOGY
- ⚡ Uses `asyncio.gather()` for simultaneous operations
- ⚡ No delays between requests
- ⚡ All tasks run in parallel
- ⚡ Completes in seconds, not minutes

### EXAMPLE: .multispam
```
- Gets all text channels in server
- For each channel:
  - Sends message 10 times immediately
  - No waiting between messages
  - All channels process simultaneously
- Completes in ~5-10 seconds regardless of channel count
```

## 📁 PROJECT STRUCTURE

```
Selfbot-nuke/
├── main.py              Main bot file
├── config.py            Configuration
├── requirements.txt     Dependencies
├── .env                 Environment variables (create this)
├── .env.example         Example env file
├── README.md            This file
└── cogs/
    ├── __init__.py
    ├── nuke.py          Nuke & create commands
    ├── spam.py          Spam commands
    └── utility.py       Utility commands
```

## 🔒 SAFETY

- ✓ Owner-only commands
- ✓ Confirmation required for dangerous operations
- ✓ Permission checks
- ✓ Error handling
- ✓ Prevents self-harm

## ⚠️ WARNING

**USE RESPONSIBLY**
- Only use on servers you own/control
- Test with small numbers first
- Follow Discord Terms of Service
- Can cause server damage if misused

## 📞 SUPPORT

- Discord.py: https://discordpy.readthedocs.io/
- Discord API: https://discord.com/developers/docs

## 📄 LICENSE

MIT License - Free to use

---

**ALPHA SELFBOT** ⚡ Lightning Fast
