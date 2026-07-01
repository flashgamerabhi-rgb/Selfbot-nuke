"""
SPAM COMMANDS - Mass message sending
All channels spam 10x each at MAXIMUM SPEED
"""
import discord
from discord.ext import commands
from config import OWNER_ID
import asyncio
import random

class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_spamming = False

    def is_owner(self, ctx):
        """Check if user is owner"""
        return ctx.author.id == OWNER_ID

    @commands.command(name='spam')
    @commands.check(is_owner)
    async def spam_message(self, ctx, count: int, channel: discord.TextChannel, *, message: str):
        """
        Spam message in a specific channel
        Usage: .spam <count> <#channel> <message>
        (MAXIMUM SPEED - NO DELAYS)
        """
        if self.is_spamming:
            await ctx.send("⚠️ Spam already in progress")
            return

        if count <= 0 or count > 5000:
            await ctx.send("❌ Count must be between 1 and 5000")
            return

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send(f"❌ No permission in {channel.mention}")
            return

        if len(message) > 2000:
            await ctx.send("❌ Message too long (max 2000)")
            return

        self.is_spamming = True
        status_msg = await ctx.send(f"⚡ Spamming {count} messages in {channel.mention}...")
        sent_count = 0

        # Send all messages simultaneously (max speed)
        tasks = []
        for i in range(count):
            msg_content = f"{message} #{i+1}"
            tasks.append(self._send_message(channel, msg_content))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        sent_count = sum(1 for r in results if r is True)

        embed = discord.Embed(
            title="✓ SPAM COMPLETE",
            description=f"Sent {sent_count} messages",
            color=discord.Color.green()
        )
        embed.add_field(name="Channel", value=channel.mention)
        embed.add_field(name="Count", value=sent_count)
        embed.add_field(name="Speed", value="⚡ MAXIMUM")
        await status_msg.edit(content=None, embed=embed)

        self.is_spamming = False

    async def _send_message(self, channel, content):
        """Helper function to send message"""
        try:
            await channel.send(content)
            return True
        except:
            return False

    @commands.command(name='spamall')
    @commands.check(is_owner)
    async def spam_all_channels(self, ctx, count: int, *, message: str):
        """
        Spam message in ALL channels
        Usage: .spamall <count> <message>
        (MAXIMUM SPEED - NO DELAYS)
        """
        if self.is_spamming:
            await ctx.send("⚠️ Spam already in progress")
            return

        if count <= 0 or count > 1000:
            await ctx.send("❌ Count must be between 1 and 1000")
            return

        self.is_spamming = True
        status_msg = await ctx.send(f"⚡ Spamming {count}x in ALL channels...")
        sent_count = 0
        channel_count = 0

        # Get all text channels
        text_channels = [ch for ch in ctx.guild.channels if isinstance(ch, discord.TextChannel)]

        # Create tasks for all channels
        tasks = []
        for channel in text_channels:
            if channel.permissions_for(ctx.guild.me).send_messages:
                channel_count += 1
                for i in range(count):
                    msg_content = f"{message} [{i+1}/{count}]"
                    tasks.append(self._send_message(channel, msg_content))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        sent_count = sum(1 for r in results if r is True)

        embed = discord.Embed(
            title="✓ MASS SPAM COMPLETE",
            description=f"Spammed {sent_count} messages",
            color=discord.Color.green()
        )
        embed.add_field(name="Channels", value=channel_count)
        embed.add_field(name="Per Channel", value=count)
        embed.add_field(name="Total Messages", value=sent_count)
        embed.add_field(name="Speed", value="⚡ MAXIMUM")
        await status_msg.edit(content=None, embed=embed)

        self.is_spamming = False

    @commands.command(name='multispam')
    @commands.check(is_owner)
    async def multi_spam(self, ctx, count: int, *, message: str):
        """
        Spam message in ALL channels 10x each
        Usage: .multispam <message>
        This spams each channel 10 times automatically
        (MAXIMUM SPEED - NO DELAYS)
        """
        if self.is_spamming:
            await ctx.send("⚠️ Spam already in progress")
            return

        self.is_spamming = True
        times_per_channel = 10  # Fixed 10 times per channel
        status_msg = await ctx.send(f"⚡ Multi-spamming ALL channels {times_per_channel}x each...")
        sent_count = 0
        channel_count = 0

        # Get all text channels
        text_channels = [ch for ch in ctx.guild.channels if isinstance(ch, discord.TextChannel)]

        # Create tasks for all channels
        tasks = []
        for channel in text_channels:
            if channel.permissions_for(ctx.guild.me).send_messages:
                channel_count += 1
                for i in range(times_per_channel):
                    msg_content = f"{message} [Ch: {channel.name}] [{i+1}/{times_per_channel}]"
                    tasks.append(self._send_message(channel, msg_content))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        sent_count = sum(1 for r in results if r is True)

        embed = discord.Embed(
            title="✓ MULTI-SPAM COMPLETE",
            description=f"Spammed {sent_count} messages total",
            color=discord.Color.green()
        )
        embed.add_field(name="Total Channels", value=channel_count)
        embed.add_field(name="Per Channel", value=times_per_channel)
        embed.add_field(name="Total Messages", value=sent_count)
        embed.add_field(name="Speed", value="⚡ MAXIMUM")
        await status_msg.edit(content=None, embed=embed)

        self.is_spamming = False

    @commands.command(name='purge')
    @commands.check(is_owner)
    async def purge_messages(self, ctx, amount: int = 10):
        """Delete messages from current channel"""
        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            await ctx.send("❌ No permission to manage messages")
            return

        if amount <= 0 or amount > 100:
            await ctx.send("❌ Amount must be between 1 and 100")
            return

        try:
            deleted = await ctx.channel.purge(limit=amount)
            await ctx.send(f"✓ Deleted {len(deleted)} messages", delete_after=5)
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(Spam(bot))
