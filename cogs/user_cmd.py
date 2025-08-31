import disnake

from disnake.ext import commands

from database.requests import get_user_info, get_all_user_tasks
from ui.windows import RegistrationWindow
from ui.embeds import tasks_info_embed
from ui.buttons import SendTasksBtn
from config.config import NOT_REGIST_ID, REGIST_ID


# -- user info --
intents = disnake.Intents.default()
intents.message_content = True
# client = disnake.Client(intents=intents)



class CmdUsers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.regist = self.bot.get_cog("RegistrationUser")
        self.on_regist = self.regist.handle_regist
        self.on_edit = self.regist.handle_edit


    # comands - regist
    @commands.slash_command(name="regist", description="зареєструватись")
    @commands.has_role(NOT_REGIST_ID)
    async def registration(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_modal(RegistrationWindow(is_edit=False, on_regist=self.on_regist))


    # comands - edit info
    @commands.slash_command(name="editinfo", description="редагувати свої дані")
    @commands.has_role(REGIST_ID)
    async def editinfo(self, inter: disnake.ApplicationCommandInteraction):
        user_data = await get_user_info(inter.author.id)
        await inter.response.send_modal(RegistrationWindow(is_edit=True, current_data=user_data, on_edit=self.on_edit))
    

    # comands - profile
    @commands.slash_command(name="profile", description="переглянути профіль")
    @commands.has_role(REGIST_ID)
    async def profile(self, inter: disnake.ApplicationCommandInteraction):
        user_data = await get_user_info(inter.author.id)
        role_names = ", ".join(role.name for role in user_data.roles)
        await inter.response.send_message(f"Username: {user_data.username} \n UserCard: {user_data.user_card} \n UserRoles: {role_names} \n UserBalance: {user_data.user_balance} \n UserXp: {user_data.user_xp} \n UserLevel: {user_data.user_level} \n UserRank: {user_data.user_rank} \n UserCountTask: {user_data.user_count_task}")


    # sends users tasks
    @commands.slash_command(name="mytasks", description="переглянути взяті завдання")
    @commands.has_role(REGIST_ID)
    async def mytasks(self, inter: disnake.ApplicationCommandInteraction):
        tasks_info = await get_all_user_tasks(inter.author.id)
        if not tasks_info:
            await inter.response.send_message("Ви  ще не маєте завдань")
            return
        
        await inter.response.send_message("Ваші завдання: ")
        for tasks in tasks_info:
            embed = tasks_info_embed(tasks.id, tasks.title, tasks.description, "Виконується", tasks.task_priority, tasks.role, tasks.price, tasks.xp)
            await inter.send(embed=embed, view=SendTasksBtn(inter.author.name, tasks.id, tasks.title, self.bot))


def setup(bot: commands.Bot):
    bot.add_cog(CmdUsers(bot))
