"""
NUKE COMMANDS - Mass delete & create channels
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
            "NUKE COMMANDS": [
                ("`.nuke`", "Delete ALL channels instantly"),
                ("`.deletechannels`", "Delete all channels (alias)"),
                ("`.deletechannels fast`", "Delete all channels at max speed"),
            ],
            "CREATE COMMANDS": [
                ("`.createchannels <count> <name>`", "Create channels with custom name"),
                ("`.create <count> <name>`", "Quick create alias"),
                ("`.multicreate <count> <name>`", "Fast multi-channel creation"),
            ],
            "SPAM COMMANDS": [
                ("`.spam <count> <#channel> <message>`", "Spam message in channel"),
                ("`.spamall <count> <message>`", "Spam message in ALL channels"),
                ("`.multispam <count> <message>`", "Spam all channels 10x each"),
            ],
            "UTILITY": [
                ("`.owner`", "Get owner info"),
                ("`.serverinfo`", "Get server information"),
                ("`.ping`", "Check bot latency"),
            ]
        }

        for category, cmds in commands_info.items():
            cmd_list = "\n".join([f"{cmd[0]:<35} {cmd[1]}" for cmd in cmds])
            embed.add_field(name=category, value=f"```\n{cmd_list}\n```", inline=False)

        embed.set_footer(text="⚡ Maximum Speed • No Delays")
        await ctx.send(embed=embed)

    @commands.command(name='nuke')
    @commands.check(is_owner)
    async def nuke_server(self, ctx):
        """Delete ALL channels instantly (MAXIMUM SPEED)"""
        if self.is_nuking:
            await ctx.send("⚠️ Nuke already in progress")
            return

        if not ctx.guild.me.guild_permissions.manage_channels:
            await ctx.send("❌ Bot doesn't have manage channels permission")
            return

        self.is_nuking = True
        msg = await ctx.send("⚠️ NUKING ALL CHANNELS! Confirm with ✓ (30s)")
        await msg.add_reaction("✓")

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

        channels = list(ctx.guild.channels)
        deleted_count = 0
        
        # Delete all channels simultaneously (max speed)
        tasks = []
        for channel in channels:
            tasks.append(self._delete_channel(channel))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        deleted_count = sum(1 for r in results if r is True)

        try:
            new_channel = await ctx.guild.create_text_channel("⚙️-nuked")
            embed = discord.Embed(
                title="✓ SERVER NUKED!",
                description=f"Deleted {deleted_count} channels",
                color=discord.Color.red()
            )
            embed.add_field(name="Speed", value="⚡ MAXIMUM")
            await new_channel.send(embed=embed)
        except:
            pass

        self.is_nuking = False

    async def _delete_channel(self, channel):
        """Helper function to delete channel"""
        try:
            await channel.delete()
            return True
        except:
            return False

    @commands.command(name='deletechannels')
    @commands.check(is_owner)
    async def delete_channels_alias(self, ctx, speed="normal"):
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

        created_count = 0
        failed_count = 0

        # Create all channels simultaneously (max speed)
        tasks = []
        for i in range(1, count + 1):
            channel_name = f"{name}-{i}".lower()[:100]
            tasks.append(self._create_channel(ctx.guild, channel_name))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        created_count = sum(1 for r in results if r is True)
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

    async def _create_channel(self, guild, name):
        """Helper function to create channel"""
        try:
            await guild.create_text_channel(name)
            return True
        except:
            return False

    @commands.command(name='create')
    @commands.check(is_owner)
    async def create_alias(self, ctx, count: int, *, name: str):
        """Quick alias for createchannels"""
        await self.create_channels(ctx, count, name=name)

    @commands.command(name='multicreate')
    @commands.check(is_owner)
    async def multi_create(self, ctx, count: int, *, name: str):
        """Fast multi-channel creation"""
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
