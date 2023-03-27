import discord
from discord.ext import commands

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=['s'],
        description="This will cause the bot to say what you say back to you!",
        brief="Repeats Words!",
        enabled=True,
        hidden=False
    )
    async def say(ctx, *what):
        """ Repeats Bullshit! """
        await ctx.send(" ".join(what))

async def setup(bot)
    await bot.add_cog(Commands(bot))