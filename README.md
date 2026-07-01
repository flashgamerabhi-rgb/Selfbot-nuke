````markdown
# 🔥 ALPHA SELFBOT - NUKE EDITION

> **High-performance Discord bot with lightning-fast nuke, spam, ban, and mass channel commands at MAXIMUM SPEED**

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![Owner Only](https://img.shields.io/badge/Owner-Only-red)

---

## ⚡ FEATURES

✅ **ONE FILE TO RUN** - Just `python run.py` to start everything  
✅ **MAXIMUM SPEED** - All operations run simultaneously (0.1s intervals)  
✅ **MASSBAN** - Ban ALL members instantly at 0.1 second intervals  
✅ **MASTER NUKE** - Delete ALL + Create + Spam in ONE command  
✅ **OWNER ONLY** - All commands restricted to owner ID  
✅ **NO AUTO-DELETE** - Messages stay visible for you  
✅ **BIG BANNER** - Huge ASCII ALPHA art on startup  
✅ **AUTO INSTALLER** - Installs dependencies automatically  
✅ **INVITE LINK** - Shows in all responses & bot status  

---

## 🚀 QUICK START

### **Step 1: Clone Repository**
```bash
git clone https://github.com/flashgamerabhi-rgb/Selfbot-nuke.git
cd Selfbot-nuke
```

### **Step 2: Create .env File**
```bash
cp .env.example .env
```

### **Step 3: Add Your Credentials**
```env
DISCORD_TOKEN=your_bot_token_here
OWNER_ID=your_discord_id_here
```

### **Step 4: Run the Launcher!**
```bash
python run.py
```

✅ **That's it!** The launcher will:
- Check .env file
- Install dependencies automatically
- Start the bot
- Show big ALPHA banner

---

## 📋 COMMANDS

### 🔥 **MASTER NUKE** - Delete All + Create + Spam

**Delete All Channels:**
```
.nuke
```
✅ Deletes ALL channels with confirmation

**Master Nuke (Delete + Create + Spam):**
```
.nuke <channel_count> <channel_name> <spam_count> <message>
```

**Examples:**
```
.nuke 50 spam 10 NUKED
.nuke 100 channel 5 SERVER HACKED
.nuke 25 test 8 DELETED
```

---

### 🔨 **CREATE COMMANDS** - Build Channels Fast

**Create Channels:**
```
.createchannels <count> <name>
```
✅ Creates channels at MAXIMUM SPEED

**Quick Aliases:**
```
.create <count> <name>
```

**Examples:**
```
.createchannels 50 spam
.create 100 channel
```

---

### 📢 **SPAM COMMANDS** - Message Blast

**Spam Single Channel:**
```
.spam <count> <#channel> <message>
```
✅ Sends message X times instantly

**Spam All Channels:**
```
.spamall <count> <message>
```
✅ Spams message X times in every channel

**Multi-Spam (10x Each):**
```
.multispam <message>
```
✅ Spams message 10 times in every channel automatically

**Examples:**
```
.spam 100 #general HELLO
.spamall 50 SPAM MESSAGE
.multispam SERVER IS DOWN
```

---

### 🚫 **MODERATION** - Ban & Kick

**Ban All Members (0.1s Intervals):**
```
.massban
```
✅ Bans ALL members instantly at 0.1 second intervals!

**Ban Single Member:**
```
.ban <@member> [reason]
```
✅ Bans a specific member

**Kick Single Member:**
```
.kick <@member> [reason]
```
✅ Kicks a specific member

**Examples:**
```
.massban
.ban @user Spam
.kick @user Violation
```

---

### ℹ️ **INFO COMMANDS**

**Show All Commands:**
```
.help
```

**Get Owner Info:**
```
.owner
```

**Get Server Info:**
```
.serverinfo
```

**Check Bot Latency:**
```
.ping
```

---

## 🏗️ SETUP GUIDE

### **1. Get Bot Token**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" → "Add Bot"
4. Copy the token
5. Enable these intents:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Guild Members Intent

### **2. Get Your Discord ID**

1. Enable Developer Mode in Discord Settings
2. Right-click your profile
3. Click "Copy User ID"

### **3. Add Bot to Server**

1. Go to OAuth2 → URL Generator
2. Select scopes: `bot`
3. Select permissions: `Administrator`
4. Copy and open the generated URL
5. Add bot to your server

### **4. Create .env File**

```env
DISCORD_TOKEN=your_actual_token_here
OWNER_ID=your_actual_id_here
```

### **5. Run the Bot!**

```bash
python run.py
```

---

## 📊 USAGE EXAMPLES

### **Example 1: Nuke Server Completely**
```
.nuke 100 temp 15 NUKED
```
✅ Deletes all channels  
✅ Creates 100 channels named "temp-1", "temp-2", etc.  
✅ Spams "NUKED" 15 times in each channel  
✅ **Completes in ~30 seconds!**

### **Example 2: Create Spam Channels**
```
.createchannels 50 spam
```
✅ Creates 50 channels instantly  

### **Example 3: Spam All Channels**
```
.multispam Hello Everyone
```
✅ Sends "Hello Everyone" 10 times in every channel at once

### **Example 4: Ban Everyone**
```
.massban
```
✅ Bans all members at 0.1 second intervals  
✅ Takes ~10 seconds to ban 100 members!

---

## ⚙️ PROJECT STRUCTURE

```
Selfbot-nuke/
├── run.py                    ⭐ LAUNCHER - Run this!
├── main.py                   Bot with big ALPHA banner
├── config.py                 Configuration
├── requirements.txt          Dependencies
├── .env                      Your credentials
├── .env.example              Example env
├── .gitignore               
├── README.md                
└── cogs/
    ├── __init__.py
    ├── nuke.py              Master nuke + create
    ├── spam.py              Spam commands
    ├── moderation.py        Ban + kick commands
    └── utility.py           Info commands
```

---

## 🔧 TECHNICAL DETAILS

### **How It Works**

- **Async Operations**: Uses `asyncio.gather()` for parallel execution
- **0.1s Intervals**: Ban operations run at 0.1 second intervals
- **No Rate Limiting**: Optimized for maximum speed
- **Owner Only**: All commands check `OWNER_ID` before executing
- **Error Handling**: Graceful error handling with user feedback

### **Speed Benchmarks**

| Operation | Members | Time |
|-----------|---------|------|
| Ban All | 100 | ~10 seconds |
| Create Channels | 50 | ~5 seconds |
| Spam All | 20 channels × 10 each | ~15 seconds |
| Master Nuke | Delete + Create + Spam | ~45 seconds |

---

## 📝 CONFIGURATION

### **.env File**
```env
DISCORD_TOKEN=your_bot_token
OWNER_ID=your_user_id
```

### **config.py**
```python
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', 0))
PREFIX = '.'
BOT_NAME = "ALPHA SELFBOT"
```

---

## 🎯 BOT STATUS

**Playing Status:**
```
Watching: https://discord.gg/6s5ZSV4ZcB
```

**Bio:**
```
🔗 https://discord.gg/6s5ZSV4ZcB
```

---

## ⚠️ IMPORTANT NOTES

- ✅ **Owner Only** - Only your ID can use commands
- ✅ **Confirmation Required** - Dangerous commands need confirmation
- ✅ **Permissions** - Bot needs admin permissions for all features
- ✅ **Legal Use** - Use only on servers you own/control
- ✅ **Discord ToS** - Follow Discord's Terms of Service
- ✅ **Responsibly** - Test with small numbers first

---

## 🔒 SECURITY

- ✅ Credentials stored in .env (not in code)
- ✅ Owner ID check on every command
- ✅ Confirmation on dangerous operations
- ✅ Error messages only shown to owner
- ✅ No sensitive data in logs

---

## 🐛 TROUBLESHOOTING

### **Bot doesn't start**
```bash
# Check .env file exists
# Check DISCORD_TOKEN is valid
# Check OWNER_ID is correct
```

### **Commands don't work**
```bash
# Make sure you're the OWNER_ID
# Make sure bot has proper permissions
# Make sure PREFIX is '.'
```

### **Ban command fails**
```bash
# Bot needs ban_members permission
# Cannot ban users higher in role hierarchy
# Cannot ban server owner
```

### **Auto-installer fails**
```bash
# Manually install: pip install -r requirements.txt
# Check Python version (3.8+)
```

---

## 📦 DEPENDENCIES

- `discord.py==2.3.2` - Discord API library
- `python-dotenv==1.0.0` - Environment variables
- `aiohttp==3.9.1` - HTTP client

Install manually:
```bash
pip install -r requirements.txt
```

---

## 🚀 PERFORMANCE

- **Nuke Command**: 100+ channels deleted in seconds
- **Create Command**: 500 channels created instantly
- **Spam Command**: 1000+ messages sent in seconds
- **Ban Command**: 100+ members banned in 10 seconds
- **No Delays**: All operations run at maximum speed

---

## 🔗 INVITE LINK

**Discord Server:** https://discord.gg/6s5ZSV4ZcB

All commands include the invite link in responses!

---

## 📄 LICENSE

MIT License - Free to use and modify

---

## 🎯 QUICK COMMAND REFERENCE

| Command | Usage | Effect |
|---------|-------|--------|
| `.nuke` | `.nuke` | Delete all channels |
| `.nuke` | `.nuke 50 spam 10 MSG` | Delete + Create + Spam |
| `.create` | `.create 50 temp` | Create 50 channels |
| `.spam` | `.spam 100 #channel MSG` | Spam channel 100x |
| `.spamall` | `.spamall 50 MSG` | Spam all channels 50x |
| `.multispam` | `.multispam MSG` | Spam all channels 10x |
| `.massban` | `.massban` | Ban ALL members |
| `.ban` | `.ban @user reason` | Ban single member |
| `.kick` | `.kick @user reason` | Kick single member |
| `.help` | `.help` | Show all commands |
| `.ping` | `.ping` | Check latency |

---

## 💡 TIPS & TRICKS

✅ Start with `.help` to see all commands  
✅ Use `.massban` for fastest member removal  
✅ Use `.nuke` for complete server wipe  
✅ Use `.multispam` for fastest spam (10x auto)  
✅ All operations show progress updates  
✅ Press Ctrl+C to stop the bot  

---

## 📞 SUPPORT

- Check Discord.py docs: https://discordpy.readthedocs.io/
- Check Discord API: https://discord.com/developers/docs
- Review .env configuration
- Check bot permissions in server

---

**ALPHA SELFBOT** ⚡ Lightning Fast • Maximum Speed • Owner Only

Last Updated: 2026-07-01  
Version: 2.0
````
