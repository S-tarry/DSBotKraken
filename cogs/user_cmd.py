import disnake

from disnake.ext import commands
from disnake import TextInputStyle
from database.database import edit_user_info, get_user_info, user_get_tasks, update_status_url
from cogs.registration import RegistrationWindow
from cogs.admin_cmd import AdminTasksBtn
# from cogs.tasks import GetTasks


# -- user info --
intents = disnake.Intents.default()
intents.message_content = True
# client = disnake.Client(intents=intents)


class CmdUsers(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # реєстрація
    @commands.slash_command(name="regist", description="зареєструватись")
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
    @commands.slash_command(name="editinfo", description="редагувати свої дані")
    async def editinfo(self, inter: disnake.ApplicationCommandInteraction):
        user_data = await get_user_info(inter.author.id)
        if user_data is None:
            await inter.response.send_message("Ви не зареєстровані! Спочатку зареєструйтесь ", ephemeral=True)
            return
        else: 
            await inter.response.send_modal(RegistrationWindow(is_edit=True, current_data=user_data))
    
    # відсилає користувачу всі завдання які він взяв 
    @commands.slash_command(name="mytasks", description="переглянути взяті завдання")
    async def mytasks(self, inter: disnake.ApplicationCommandInteraction):
        user_id = inter.author.id 
        tasks_info = await user_get_tasks(user_id)
        priority_colors = {
                "Low": disnake.Color.blue(),
                "Medium": disnake.Color.orange(), 
                "High": disnake.Color.red()
        }
        print(tasks_info)
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
                    color=priority_colors.get(tasks_priority, disnake.Color.greyple())
                )
                embed.add_field(name="Статус", value=tasks_status, inline=True)
                embed.add_field(name="Пріоритет", value=tasks_priority, inline=True)
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name="Ціна", value=tasks_total_price, inline=True)
                embed.add_field(name="Досвід", value=tasks_total_xp, inline=True)
                await inter.send(embed=embed, view=SendTasksBtn(inter.author.name, tasks_id, tasks_title, self.bot), content="Ваші завдання")


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
