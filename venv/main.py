import discord
from discord import Intents
from discord.ext import commands, tasks
from discord.utils import get
import settings
from cogs.commands import Commands

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    bot = commands.Bot(command_prefix=">", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")


        for cogs_file in settings.COGS_DIR.glob("*.py"):
            if cogs_file != "__init__.py":
                await bot.load_extension(f"cogs.{cogs_file.name[:-3]}")

        @bot.command()
        async def reload(ctx, cog: str):
            role = discord.utils.get(ctx.guild.roles, id=1073915462712303706)
            if role in ctx.message.author.roles:
                await bot.reload_extension(f"cogs.{cog.lower()}")
                await ctx.send(f"ADMIN DEBUG COMMAND RECEIVED :: {ctx.message.author.mention} has requested the reloading of {cog}.py")
                print(f"ADMIN DEBUG COMMAND RECEIVED : {ctx.message.author.nick} requested reload of {cog}.py")
            else:
                await ctx.send(f"ADMIN DEBUG COMMAND REJECTED :: Fuck off {ctx.message.author.mention}.")
                print(f"ADMIN DEBUG COMMANDS REFUSED : {ctx.message.author.nick} attempted to reload {cog}.py")

    bot.run(settings.DICKSWORD_TOKE, root_logger=True)


if __name__ == "__main__":
    run()