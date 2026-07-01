"""
MODERATION COMMANDS - Mass ban with 0.1 second intervals
Owner only
"""
import discord
from discord.ext import commands
from config import OWNER_ID
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_banning = False

    def is_owner(self, ctx):
        """Check if user is owner"""
        return ctx.author.id == OWNER_ID

    @commands.command(name='massban')
    @commands.check(is_owner)
    async def mass_ban(self, ctx):
        """
        BAN ALL MEMBERS AT ONCE - 0.1 SECOND INTERVALS
        Owner only
        """
        if self.is_banning:
            msg = await ctx.send("⚠️ Ban in progress")
            return

        if not ctx.guild.me.guild_permissions.ban_members:
            msg = await ctx.send("❌ No ban permission")
            return

        # Delete command message
        try:
            await ctx.message.delete()
        except:
            pass

        # Confirmation
        confirm_msg = await ctx.send("⚠️ BAN ALL MEMBERS? React ✓ (30s)")
        await confirm_msg.add_reaction("✓")

        try:
            await self.bot.wait_for(
                'reaction_add',
                check=lambda r, u: u.id == ctx.author.id and str(r.emoji) == "✓",
                timeout=30
            )
        except asyncio.TimeoutError:
            try:
                await confirm_msg.delete()
            except:
                pass
            return

        try:
            await confirm_msg.delete()
        except:
            pass

        self.is_banning = True
        status_msg = await ctx.send("⚡ BANNING ALL MEMBERS...")
        banned_count = 0
        failed_count = 0

        # Get all members
        members = []
        async for member in ctx.guild.fetch_members(limit=None):
            if member.id != OWNER_ID and member.id != self.bot.user.id:
                members.append(member)

        total_members = len(members)

        # Ban all members with 0.1 second interval
        for i, member in enumerate(members):
            try:
                await member.ban(reason="Mass ban by owner")
                banned_count += 1
                # 0.1 second delay between bans
                await asyncio.sleep(0.1)
            except Exception as e:
                failed_count += 1
                await asyncio.sleep(0.1)

            # Update progress every 10 bans
            if (i + 1) % 10 == 0 or (i + 1) == total_members:
                await status_msg.edit(content=f"⚡ BANNING... {i+1}/{total_members} | Banned: {banned_count}")

        embed = discord.Embed(
            title="✓ MASS BAN COMPLETE",
            description=f"Banned {banned_count} members",
            color=discord.Color.red()
        )
        embed.add_field(name="Total Members", value=total_members)
        embed.add_field(name="Banned", value=banned_count)
        embed.add_field(name="Failed", value=failed_count)
        embed.add_field(name="Speed", value="⚡ 0.1s intervals")
        embed.add_field(name="🔗 Invite", value="https://discord.gg/6s5ZSV4ZcB", inline=False)
        
        await status_msg.edit(content=None, embed=embed)

        self.is_banning = False

    @commands.command(name='ban')
    @commands.check(is_owner)
    async def ban_user(self, ctx, member: discord.Member, *, reason="No reason"):
        """Ban a single member - OWNER ONLY"""
        if not ctx.guild.me.guild_permissions.ban_members:
            msg = await ctx.send("❌ No ban permission")
            return

        if member.id == OWNER_ID:
            msg = await ctx.send("❌ Cannot ban owner")
            return

        try:
            await ctx.message.delete()
        except:
            pass

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="✓ MEMBER BANNED",
                description=f"{member.mention} banned",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="🔗 Invite", value="https://discord.gg/6s5ZSV4ZcB", inline=False)
            msg = await ctx.send(embed=embed)
        except Exception as e:
            msg = await ctx.send(f"❌ Error: {e}")

    @commands.command(name='kick')
    @commands.check(is_owner)
    async def kick_user(self, ctx, member: discord.Member, *, reason="No reason"):
        """Kick a single member - OWNER ONLY"""
        if not ctx.guild.me.guild_permissions.kick_members:
            msg = await ctx.send("❌ No kick permission")
            return

        if member.id == OWNER_ID:
            msg = await ctx.send("❌ Cannot kick owner")
            return

        try:
            await ctx.message.delete()
        except:
            pass

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✓ MEMBER KICKED",
                description=f"{member.mention} kicked",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="🔗 Invite", value="https://discord.gg/6s5ZSV4ZcB", inline=False)
            msg = await ctx.send(embed=embed)
        except Exception as e:
            msg = await ctx.send(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
