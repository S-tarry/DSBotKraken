import disnake

from disnake.ext import commands
from disnake import TextInputStyle
from database.database import edit_user_info, get_user_info, user_get_tasks
from cogs.registration import RegistrationWindow

# -- user info --
# intents = disnake.Intents.default()
# intents.message_content = True
# client = disnake.Client(intents=intents)


class CmdUsers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # реєстрація
    @commands.slash_command(name="regist", description="Почати реєстрацію")
    async def registration(self, inter: disnake.ApplicationCommandInteraction):
        # тимчасове поки не з'явитьсяя перевірка на доступ до команд
        # ------------------------------------------------------------
        user_data = await get_user_info(inter.author.id)
        if user_data is not None:
            await inter.response.send_message("Ви вже зареєстровані", ephemeral=True)
            return
        # ------------------------------------------------------------
        await inter.response.send_modal(RegistrationWindow())

    # редагування інформації
    @commands.slash_command(name="editinfo", description="редагування даних")
    async def editinfo(self, inter: disnake.ApplicationCommandInteraction):
        user_data = await get_user_info(inter.author.id)
        if user_data is None:
            await inter.response.send_message("Ви не зареєстровані! Спочатку зареєструйтесь ", ephemeral=True)
            return
        else: 
            await inter.response.send_modal(RegistrationWindow(is_edit=True, current_data=user_data))
    

    @commands.slash_command(name="mytasks", description="перегляд взятих завдань")
    async def mytasks(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id 
        tasks_info = await user_get_tasks(user_id)
        print(tasks_info)
        if tasks_info is None:
            await inter.response.send_message("Ви  ще не маєте завдань")
            return
        else:
            await inter.response.send_message("Ваші завдання: ")


def setup(bot: commands.Bot):
    bot.add_cog(CmdUsers(bot))
