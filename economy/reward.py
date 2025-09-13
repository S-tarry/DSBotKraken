import disnake

from disnake.ext import commands

from database.requests import get_user_info, delete_compated_user_tasks
from .levels import add_xp_to_user_xp
from .rangs import update_user_rank
from .salary import add_money_to_balance
# from config.config import EVENTS_CHANNEL


async def reward_user(user_id, task_id, bot: commands.Bot):
    await update_user_rank(user_id, bot)
    await get_user_info(user_id)
    await add_xp_to_user_xp(user_id, task_id, bot)
    await add_money_to_balance(user_id, task_id)
    await delete_compated_user_tasks(task_id)

    # user = await bot.fetch_user(user_id)
    # if user:
    #     await user.send(f"Ваше завдання підтверджено! Баланс та xp додано!")
