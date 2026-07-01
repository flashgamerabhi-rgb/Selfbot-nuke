"""
Utility commands
"""
import discord
from discord.ext import commands
from config import OWNER_ID

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, ctx):
        """Check if user is owner"""
        return ctx.author.id == OWNER_ID

    @commands.command(name='stats')
    @commands.check(is_owner)
    async def show_stats(self, ctx):
        """Show bot statistics"""
        embed = discord.Embed(
            title="📊 BOT STATISTICS",
            color=discord.Color.blue()
        )
        embed.add_field(name="Server Name", value=ctx.guild.name)
        embed.add_field(name="Members", value=ctx.guild.member_count)
        embed.add_field(name="Channels", value=len(ctx.guild.channels))
        embed.add_field(name="Roles", value=len(ctx.guild.roles))
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed)

    @commands.command(name='test')
    @commands.check(is_owner)
    async def test_command(self, ctx):
        """Test bot connection"""
        embed = discord.Embed(
            title="✓ BOT ONLINE",
            description="ALPHA SELFBOT is running",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
