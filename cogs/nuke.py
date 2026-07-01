"""
NUKE COMMANDS - Master nuke with create, spam all in one
All commands run at maximum speed
"""
import discord
from discord.ext import commands
from config import OWNER_ID
import asyncio
import random

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_nuking = False
        self.is_creating = False

    def is_owner(self, ctx):
        """Check if user is owner"""
        return ctx.author.id == OWNER_ID

    @commands.command(name='help')
    @commands.check(is_owner)
    async def show_help(self, ctx):
        """Show all commands"""
        embed = discord.Embed(
            title="🚀 ALPHA SELFBOT - COMMANDS",
            description="All nuke and spam commands",
            color=discord.Color.red()
        )

        commands_info = {
            "MASTER NUKE": [
                ("`.nuke <count> <channel_name> <spam_count> <message>`", "DELETE ALL + CREATE + SPAM ALL"),
                ("`.nuke`", "Delete ALL channels only"),
            ],
            "CREATE COMMANDS": [
                ("`.createchannels <count> <name>`", "Create channels with custom name"),
                ("`.create <count> <name>`", "Quick create alias"),
            ],
            "SPAM COMMANDS": [
                ("`.spam <count> <#channel> <message>`", "Spam message in channel"),
                ("`.spamall <count> <message>`", "Spam message in ALL channels"),
            ],
            "UTILITY": [
                ("`.owner`", "Get owner info"),
                ("`.serverinfo`", "Get server information"),
                ("`.ping`", "Check bot latency"),
            ]
        }

        for category, cmds in commands_info.items():
            cmd_list = "\n".join([f"{cmd[0]:<50} {cmd[1]}" for cmd in cmds])
            embed.add_field(name=category, value=f"```\n{cmd_list}\n```", inline=False)

        embed.set_footer(text="⚡ Maximum Speed • No Delays • All at Once")
        await ctx.send(embed=embed)

    @commands.command(name='nuke')
    @commands.check(is_owner)
    async def nuke_server(self, ctx, channel_count: int = None, channel_name: str = None, spam_count: int = None, *, message: str = None):
        """
        MASTER NUKE COMMAND - Do everything at once!
        
        Usage 1 (Delete only):
        .nuke
        
        Usage 2 (Delete + Create + Spam):
        .nuke <channel_count> <channel_name> <spam_count> <message>
        
        Examples:
        .nuke 50 spam 10 NUKED
        .nuke 100 channel 5 SERVER NUKED
        """
        if self.is_nuking:
            await ctx.send("⚠️ Nuke already in progress")
            return

        if not ctx.guild.me.guild_permissions.manage_channels:
            await ctx.send("❌ Bot doesn't have manage channels permission")
            return

        # If no parameters, just delete channels
        if channel_count is None:
            await self._delete_all_channels(ctx)
            return

        # Validate parameters
        if channel_count <= 0 or channel_count > 500:
            await ctx.send("❌ Channel count must be between 1 and 500")
            return

        if spam_count is None or spam_count <= 0 or spam_count > 100:
            await ctx.send("❌ Spam count must be between 1 and 100")
            return

        if not message:
            await ctx.send("❌ Message required")
            return

        if len(message) > 2000:
            await ctx.send("❌ Message too long (max 2000)")
            return

        # Start the master nuke
        self.is_nuking = True
        
        # Confirmation
        confirm_msg = await ctx.send(
            f"⚠️ **MASTER NUKE ACTIVATED**\n"
            f"1️⃣ Delete ALL channels\n"
            f"2️⃣ Create {channel_count} channels named '{channel_name}'\n"
            f"3️⃣ Spam '{message}' {spam_count}x in each channel\n\n"
            f"React ✓ to confirm (30s)"
        )
        await confirm_msg.add_reaction("✓")

        try:
            reaction, user = await self.bot.wait_for(
                'reaction_add',
                check=lambda r, u: u.id == ctx.author.id and str(r.emoji) == "✓",
                timeout=30
            )
        except asyncio.TimeoutError:
            await ctx.send("❌ Nuke cancelled")
            self.is_nuking = False
            return

        # Start progress
        progress_msg = await ctx.send("🚀 NUKE STARTED - MAXIMUM SPEED MODE\n⏳ Deleting all channels...")

        # STEP 1: Delete all channels
        deleted_count = await self._delete_all_channels_async(ctx)
        await progress_msg.edit(content=f"🚀 NUKE IN PROGRESS\n✓ Deleted {deleted_count} channels\n⏳ Creating {channel_count} channels...")

        # STEP 2: Create all channels
        created_channels = await self._create_all_channels_async(ctx.guild, channel_count, channel_name)
        created_count = len(created_channels)
        await progress_msg.edit(content=f"🚀 NUKE IN PROGRESS\n✓ Deleted {deleted_count} channels\n✓ Created {created_count} channels\n⏳ Spamming messages ({spam_count}x each)...")

        # STEP 3: Spam all channels
        spammed_count = await self._spam_all_channels_async(created_channels, spam_count, message, channel_name)
        
        # Final summary
        embed = discord.Embed(
            title="🔥 MASTER NUKE COMPLETE! 🔥",
            description="All operations completed at maximum speed",
            color=discord.Color.red()
        )
        embed.add_field(name="1️⃣ Channels Deleted", value=deleted_count, inline=False)
        embed.add_field(name="2️⃣ Channels Created", value=created_count, inline=False)
        embed.add_field(name="3️⃣ Messages Spammed", value=f"{spammed_count} messages ({spam_count}x in each of {created_count} channels)", inline=False)
        embed.add_field(name="⚡ Speed", value="MAXIMUM - All at Once", inline=False)
        embed.add_field(name="⏱️ Status", value="✅ 100% Complete", inline=False)
        
        await progress_msg.edit(content=None, embed=embed)
        self.is_nuking = False

    async def _delete_all_channels(self, ctx):
        """Delete all channels (simple method with confirmation)"""
        msg = await ctx.send("⚠️ DELETE ALL CHANNELS! Confirm with ✓ (30s)")
        await msg.add_reaction("✓")

        try:
            reaction, user = await self.bot.wait_for(
                'reaction_add',
                check=lambda r, u: u.id == ctx.author.id and str(r.emoji) == "✓",
                timeout=30
            )
        except asyncio.TimeoutError:
            await ctx.send("❌ Cancelled")
            return

        deleted_count = await self._delete_all_channels_async(ctx)

        try:
            new_channel = await ctx.guild.create_text_channel("⚙️-nuked")
            embed = discord.Embed(
                title="✓ SERVER NUKED!",
                description=f"Deleted {deleted_count} channels",
                color=discord.Color.red()
            )
            await new_channel.send(embed=embed)
        except:
            pass

    async def _delete_all_channels_async(self, ctx):
        """Delete all channels asynchronously"""
        channels = list(ctx.guild.channels)
        tasks = [self._delete_channel(channel) for channel in channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r is True)

    async def _delete_channel(self, channel):
        """Helper function to delete channel"""
        try:
            await channel.delete()
            return True
        except:
            return False

    async def _create_all_channels_async(self, guild, count, name):
        """Create all channels asynchronously and return list"""
        tasks = []
        for i in range(1, count + 1):
            channel_name = f"{name}-{i}".lower()[:100]
            tasks.append(self._create_channel_async(guild, channel_name))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if r is not None]

    async def _create_channel_async(self, guild, name):
        """Helper function to create channel and return channel object"""
        try:
            channel = await guild.create_text_channel(name)
            return channel
        except:
            return None

    async def _spam_all_channels_async(self, channels, spam_count, message, channel_name):
        """Spam message in all channels asynchronously"""
        tasks = []
        total_messages = 0

        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                for i in range(spam_count):
                    msg_content = f"{message} [{i+1}/{spam_count}]"
                    tasks.append(self._send_message(channel, msg_content))
                    total_messages += 1

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r is True)

    async def _send_message(self, channel, content):
        """Helper function to send message"""
        try:
            await channel.send(content)
            return True
        except:
            return False

    @commands.command(name='deletechannels')
    @commands.check(is_owner)
    async def delete_channels_alias(self, ctx):
        """Delete all channels (Alias for nuke)"""
        await self.nuke_server(ctx)

    @commands.command(name='createchannels')
    @commands.check(is_owner)
    async def create_channels(self, ctx, count: int, *, name: str):
        """Create multiple channels at maximum speed"""
        if self.is_creating:
            await ctx.send("⚠️ Channel creation already in progress")
            return

        if not ctx.guild.me.guild_permissions.manage_channels:
            await ctx.send("❌ Bot doesn't have manage channels permission")
            return

        if count <= 0 or count > 500:
            await ctx.send("❌ Count must be between 1 and 500")
            return

        self.is_creating = True
        status_msg = await ctx.send(f"⚡ Creating {count} channels named '{name}'...")

        # Create all channels simultaneously
        tasks = []
        for i in range(1, count + 1):
            channel_name = f"{name}-{i}".lower()[:100]
            tasks.append(self._create_channel_async(ctx.guild, channel_name))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        created_count = sum(1 for r in results if r is not None)
        failed_count = count - created_count

        embed = discord.Embed(
            title="✓ CHANNELS CREATED",
            description=f"Successfully created {created_count} channels",
            color=discord.Color.green()
        )
        embed.add_field(name="Channel Name", value=name)
        embed.add_field(name="Created", value=created_count)
        embed.add_field(name="Failed", value=failed_count)
        embed.add_field(name="Speed", value="⚡ MAXIMUM")
        await status_msg.edit(content=None, embed=embed)

        self.is_creating = False

    @commands.command(name='create')
    @commands.check(is_owner)
    async def create_alias(self, ctx, count: int, *, name: str):
        """Quick alias for createchannels"""
        await self.create_channels(ctx, count, name=name)

    @commands.command(name='owner')
    @commands.check(is_owner)
    async def show_owner(self, ctx):
        """Show owner information"""
        owner = await self.bot.fetch_user(OWNER_ID)
        embed = discord.Embed(
            title="👑 OWNER",
            color=discord.Color.gold()
        )
        embed.add_field(name="Username", value=owner.name)
        embed.add_field(name="ID", value=owner.id)
        embed.add_field(name="Status", value="🟢 Online")
        embed.set_thumbnail(url=owner.avatar.url if owner.avatar else None)
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo')
    @commands.check(is_owner)
    async def server_info(self, ctx):
        """Get server information"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Server ID", value=guild.id)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command(name='ping')
    @commands.check(is_owner)
    async def ping(self, ctx):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 PING",
            description=f"⚡ {latency}ms",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Nuke(bot))
