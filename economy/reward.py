import disnake

from disnake.ext import commands

from .levels import add_xp_to_user_xp
from .rangs import update_user_rank
from .salary import add_money_to_balance
from config.config import EVENTS_CHANEL


async def reward_user(user_id, task_id, bot: commands.Bot):
    xp_added = await add_xp_to_user_xp(user_id, task_id)
    runk_update = await update_user_rank(user_id)
    await add_money_to_balance(user_id, task_id)

    user = await bot.fetch_user(user_id)
    if user:
        await user.send(f"Ваше завдання підтверджено! Баланс та xp оновлено!")
    
    if runk_update:
        channel = bot.get_channel(EVENTS_CHANEL)
        if channel:
            await channel.send(f"Користувач - {user.username} повишений до рангу: {user.user_rank}")
