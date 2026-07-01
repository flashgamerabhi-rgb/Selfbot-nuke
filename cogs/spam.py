"""
SPAM COMMANDS - Mass message sending
All commands run at maximum speed
Owner only visibility
"""
import discord
from discord.ext import commands
from config import OWNER_ID
import asyncio

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
        Spam message in a specific channel - OWNER ONLY
        Usage: .spam <count> <#channel> <message>
        (MAXIMUM SPEED - NO DELAYS)
        """
        if self.is_spamming:
            msg = await ctx.send("⚠️ Spam in progress")
            return

        if count <= 0 or count > 5000:
            msg = await ctx.send("❌ Count: 1-5000")
            return

        if not channel.permissions_for(ctx.guild.me).send_messages:
            msg = await ctx.send(f"❌ No permission in {channel.mention}")
            return

        if len(message) > 2000:
            msg = await ctx.send("❌ Message too long (max 2000)")
            return

        # Delete command message
        try:
            await ctx.message.delete()
        except:
            pass

        self.is_spamming = True
        status_msg = await ctx.send(f"⚡ Spamming {count}x in {channel.mention}...")

        # Send all messages simultaneously (MAXIMUM SPEED)
        tasks = []
        for i in range(count):
            msg_content = f"{message}"
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
        embed.add_field(name="🔗 Invite", value="https://discord.gg/6s5ZSV4ZcB", inline=False)
        
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
        Spam message in ALL channels - OWNER ONLY
        Usage: .spamall <count> <message>
        (MAXIMUM SPEED - NO DELAYS)
        """
        if self.is_spamming:
            msg = await ctx.send("⚠️ Spam in progress")
            return

        if count <= 0 or count > 1000:
            msg = await ctx.send("❌ Count: 1-1000")
            return

        # Delete command message
        try:
            await ctx.message.delete()
        except:
            pass

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
                    msg_content = f"{message}"
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
        embed.add_field(name="🔗 Invite", value="https://discord.gg/6s5ZSV4ZcB", inline=False)
        
        await status_msg.edit(content=None, embed=embed)

        self.is_spamming = False

    @commands.command(name='multispam')
    @commands.check(is_owner)
    async def multi_spam(self, ctx, *, message: str):
        """
        Spam message in ALL channels 10x each - OWNER ONLY
        Usage: .multispam <message>
        (MAXIMUM SPEED - NO DELAYS)
        """
        if self.is_spamming:
            msg = await ctx.send("⚠️ Spam in progress")
            return

        # Delete command message
        try:
            await ctx.message.delete()
        except:
            pass

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
                    msg_content = f"{message}"
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
        embed.add_field(name="🔗 Invite", value="https://discord.gg/6s5ZSV4ZcB", inline=False)
        
        await status_msg.edit(content=None, embed=embed)

        self.is_spamming = False

    @commands.command(name='purge')
    @commands.check(is_owner)
    async def purge_messages(self, ctx, amount: int = 10):
        """Delete messages from current channel - OWNER ONLY"""
        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            msg = await ctx.send("❌ No permission to manage messages")
            return

        if amount <= 0 or amount > 100:
            msg = await ctx.send("❌ Amount: 1-100")
            return

        try:
            await ctx.message.delete()
        except:
            pass

        try:
            deleted = await ctx.channel.purge(limit=amount)
            embed = discord.Embed(
                title="✓ PURGED",
                description=f"Deleted {len(deleted)} messages",
                color=discord.Color.blue()
            )
            embed.add_field(name="🔗 Invite", value="https://discord.gg/6s5ZSV4ZcB", inline=False)
            msg = await ctx.send(embed=embed)
        except Exception as e:
            msg = await ctx.send(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(Spam(bot))
