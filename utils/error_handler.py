import logging
import traceback
import disnake

from disnake.ext import commands

logger = logging.getLogger("KrakenBotLoger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("info/KrakenBot.log", encoding="utf8")
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(file_handler)


async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: Exception):
    error_info = f"Користувач: '{inter.author}'. Команда: '{inter.application_command.name}'"

    if isinstance(error, commands.MissingRole):
        await inter.response.send_message("Ви не можете знову використовувати дану команду.", ephemeral=True)
        logger.warning(f"В користувача немає ролі. {error_info}")
    elif isinstance(error, commands.MissingPermissions):
        await inter.response.send_message("У вас немає прав для використання команди.", ephemeral=True)
        logger.warning(f"Користувач немає прав. {error_info}")
    elif isinstance(error, commands.BadArgument):
        await inter.response.send_message("Дані введено неправильно.", ephemeral=True)
        logger.warning(f"Дані введено напривильно. {error_info}", ephemeral=True)
    elif isinstance(error, commands.CommandNotFound):
        await inter.response.send_message("Такої команди не існує.", ephemeral=True)
        logger.warning(f"Немає введеної команди. {error_info}", ephemeral=True)
    else:
        await inter.response.send_message("Невідома помилка.", ephemeral=True)
        logger.error(f"Невідома помилка. {error_info} | {error}\n{traceback.format_exc()}")


async def on_command_error(ctx, error):
    error_info = f"Користувач: '{ctx.author}'. Команда: '{ctx.command}'"

    if isinstance(error, commands.CommandNotFound):
        logger.warning(f"Немає введеної команди. {error_info}")
    else:
        logger.error(f"Невідома помилка. {error_info} | {error}\n{traceback.format_exc()}")


async def send_error_or_info(bot, message: str, channel_id: int, file: disnake.File = None, embed: disnake.Embed = None):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message, file=file, embed=embed)
