import disnake
import traceback

from disnake.ext import commands

from config.config import ERROR_CHANNEL
from utils.error_handler import logger, send_error_or_info
from config.config import ADMIN_ID, SERVER_ID, NOT_REGIST_ID, BOT_ID, INFORM_ADMIN_CHANNEL
from database.requests import add_all_roles_into_db



class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(SERVER_ID)
        try:
            if guild:
                await add_all_roles_into_db(guild.roles, [ADMIN_ID, BOT_ID])
        except Exception as e:
            await send_error_or_info(self.bot, "Виникла помилка при додаванні ролей в БД.", ERROR_CHANNEL)
            logger.error(f"Помилка при додаванні всіх ролей в БД. {e}\n{traceback.format_exc()}")


    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        role = member.guild.get_role(NOT_REGIST_ID)
        if role:
            await member.add_roles(role)
        channel = disnake.utils.get(member.guild.text_channels, name="rules")
        if channel:
            thread = await channel.create_thread(
                name=f"Реєстрація {member.name}",
                type=disnake.ChannelType.private_thread,
                invitable=False
            )
            await thread.add_user(member)
            await thread.send("**Привіт! 👋\nВітаємо на нашому сервері.**\nЯ *RKKS Bot*, твій помічник на сервері.\nЩоб розпочати, використай команду `/regist`\n>Після реєстації ти отримаєш доступ до всіх каналів та бонусів!")


    @commands.Cog.listener()
    async def on_guild_role_create(self, role: disnake.Role):
        await add_all_roles_into_db([role], [ADMIN_ID, BOT_ID])
        await send_error_or_info(self.bot, f"Нову роль - {role.name} додано в БД", INFORM_ADMIN_CHANNEL)



def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))
