import disnake

from disnake.ext import commands
from disnake import TextInputStyle
from database.database import get_price_xp_tasks, get_user_info, update_user_info_xp_balance
# from cogs.registration import RegistrationWindow



intents = disnake.Intents.default()
intents.message_content = True



# нарахування досвіду і монет
class Reward(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def reward_user(task_id, user_id):
        price_xp_info = await get_price_xp_tasks(task_id)
        price, xp = price_xp_info

        user_info = await get_user_info(user_id)
        current_balance = user_info[7]
        current_xp = user_info[4]

        new_balance = current_balance + price
        new_xp = current_xp + xp


        await update_user_info_xp_balance(user_id, new_balance, new_xp)


def setup(bot: commands.Bot):
    bot.add_cog(Reward(bot))
