import disnake

from disnake.ext import commands
from disnake import Permissions

from config.config import NOT_REGIST_ID, REGIST_ID
from database.requests import get_user_info, get_all_user_tasks
from ui.windows import RegistrationWindow
from ui.embeds import tasks_info_embed, user_info_embed
from ui.buttons import SendTasksBtn



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
    @commands.slash_command(name="editinfo", description="редагувати свої дані", default_member_permissions=Permissions(view_channel=True))
    @commands.has_role(REGIST_ID)
    async def editinfo(self, inter: disnake.ApplicationCommandInteraction):
        user_data = await get_user_info(inter.author.id)
        await inter.response.send_modal(RegistrationWindow(is_edit=True, current_data=user_data, on_edit=self.on_edit))
    

    # comands - profile
    @commands.slash_command(name="profile", description="переглянути свій профіль")
    @commands.has_role(REGIST_ID)
    async def profile(self, inter: disnake.ApplicationCommandInteraction):
        user_data = await get_user_info(inter.author.id)
        embed = user_info_embed(user_data.username, user_data.user_card, user_data.roles, user_data.user_balance, 
                                user_data.user_xp, user_data.user_level, user_data.user_rank, user_data.user_count_task)
        await inter.response.send_message(embed=embed, ephemeral=True)


    # sends users tasks
    @commands.slash_command(name="mytasks", description="переглянути взяті завдання")
    @commands.has_role(REGIST_ID)
    async def mytasks(self, inter: disnake.ApplicationCommandInteraction):
        tasks_info = await get_all_user_tasks(inter.author.id)
        if not tasks_info:
            await inter.response.send_message("Ви ще не маєте завдань.", ephemeral=True)
            return
        
        await inter.response.send_message("Ваші завдання", ephemeral=True)
        for tasks in tasks_info:
            embed = tasks_info_embed(tasks.id, tasks.title, tasks.description, "Виконується", tasks.task_priority, tasks.role, tasks.price, tasks.xp)
            await inter.send(embed=embed, view=SendTasksBtn(inter.author.name, tasks.id, tasks.title, self.bot), ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(CmdUsers(bot))
