import disnake

from disnake.ext import commands
from disnake import TextInputStyle
from database.database import user_get_tasks, update_status_url
from database.requests import get_user_info
from ui.windows import RegistrationWindow
from cogs.admin_cmd import AdminTasksBtn
from cogs.config import NOT_REGIST_ID, REGIST_ID, PRIORITY_COLORS


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


    # відсилає користувачу всі завдання які він взяв 
    @commands.slash_command(name="mytasks", description="переглянути взяті завдання")
    @commands.has_role(REGIST_ID)
    async def mytasks(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id 
        tasks_info = await user_get_tasks(user_id)
        # priority_colors = {
        #         "Low": disnake.Color.blue(),
        #         "Medium": disnake.Color.orange(), 
        #         "High": disnake.Color.red()
        # }
        # print(tasks_info)
        if not tasks_info:
            await inter.response.send_message("Ви  ще не маєте завдань")
            return
        else:
            # await inter.response.send_message("Ваші завдання: ")
            for tasks in tasks_info:
                tasks_id, tasks_title, tasks_description, tasks_status, tasks_priority, tasks_role, tasks_total_price, tasks_total_xp, user_task_status = tasks
            
                embed = disnake.Embed(
                    title=f"{tasks_title}",
                    description=f"{tasks_description}",
                    color=PRIORITY_COLORS.get(tasks_priority, disnake.Color.greyple())
                )
                embed.add_field(name="Статус", value=tasks_status, inline=True)
                embed.add_field(name="Пріоритет", value=tasks_priority, inline=True)
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name="Ціна", value=tasks_total_price, inline=True)
                embed.add_field(name="Досвід", value=tasks_total_xp, inline=True)
                await inter.send(embed=embed, view=SendTasksBtn(inter.author.name, tasks_id, tasks_title, self.bot))



# кнопки для відправки завдань на перевірку
class SendTasksBtn(disnake.ui.View):
    def __init__(self, username, task_id, task_title, bot: commands.Bot):
        self.bot = bot
        self.username = username
        self.task_id = task_id
        self.task_title = task_title

        super().__init__(timeout=None)
        
    @disnake.ui.button(label="Відправити на перевірку", style=disnake.ButtonStyle.green, custom_id="sendview")
    async def sendview(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(AdditionalyInfoWindow(self.task_id, self.task_title, self.username, self.bot))
        await inter.message.delete()
        


# вікно для введення посилання на виконане завдання та додаткової інформації
class AdditionalyInfoWindow(disnake.ui.Modal):
    def __init__(self, task_id, task_title, username, bot):
        self.bot = bot
        self.task_id = task_id
        self.task_title = task_title
        self.username = username

        components = [
            disnake.ui.TextInput(
                label="Посилання на виконане завдання ",
                placeholder="https://example.com/your-task",
                custom_id="link",
                style=TextInputStyle.short,
                required=True,
            ),
            disnake.ui.TextInput(
                label="Додаткова інформація",
                placeholder="додатково",
                custom_id="additionaly",
                style=TextInputStyle.short,
                required=False,
            ),
        ]
        title = "Інформація до завдання"
        super().__init__(title=title, components=components)
    
    async def callback(self, inter: disnake.ModalInteraction):
        await inter.response.defer()
        get_cog = self.bot.get_cog('GetTasks')

        link_to_task = inter.text_values["link"]
        additionaly_description = inter.text_values["additionaly"]
        await update_status_url(self.task_id, "Не розпочато", link_to_task)

        await get_cog.update_task_status_in_excel(self.task_title, "Виконується", link_to_task)
        channel_id = 1403835386576375960
        channel = self.bot.get_channel(channel_id)

        await channel.send(f"Користувач - {inter.author.name}.\n Виконав завдання - {self.task_title}. \n Опис до завдання: {additionaly_description}", view=AdminTasksBtn(self.task_id, inter.author.id, self.task_title, link_to_task, self.bot,))
        await inter.followup.send("Завдання надіслано на перевірку! Очікуйте відповідь.")
    


def setup(bot: commands.Bot):
    bot.add_cog(CmdUsers(bot))
