import os
import disnake

from dotenv import load_dotenv
from disnake.ext import commands
from database.database import init_db
from database.models import async_main
from config.config import BOT_TOKEN

load_dotenv()
bot = commands.Bot(command_prefix='.', help_command=None,
                   intents=disnake.Intents.all())


@bot.event
async def on_ready():
    await async_main()
    await init_db()
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


bot.run(BOT_TOKEN)
