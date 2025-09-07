import os
import disnake
import asyncio

from disnake.ext import commands

from database.models import async_main
from config.config import BOT_TOKEN
from utils.error_handler import on_slash_command_error, on_command_error

bot = commands.Bot(command_prefix='+', help_command=None, intents=disnake.Intents.all())
bot.on_slash_command_error = on_slash_command_error
bot.on_command_error = on_command_error



async def main():
    await async_main()
    print("БД створена")


@bot.command()
@commands.is_owner()
async def load(inter, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
@commands.is_owner()
async def unload(inter, extension):
    bot.unload_extension(f"cogs.{extension}")

@bot.command()
@commands.is_owner()
async def reload(inter, extension):
    bot.reload_extension(f"cogs.{extension}")

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


if __name__ == "__main__":
    asyncio.run(main()) 
    bot.run(BOT_TOKEN)