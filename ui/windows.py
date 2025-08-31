import disnake
import os

from disnake.ext import commands
from disnake.ui import Select, View
from disnake import TextInputStyle

from dotenv import load_dotenv
from database.database import get_user_info, edit_user_info
from database.requests import update_user_tasks
from config.config import ROLES, REGIST_ID, NOT_REGIST_ID, ADMIN_CHANNEL
from cogs.tasks import GetTasks
# from ui.buttons import ConfirmCancelTaskBtn

intents = disnake.Intents.default()
intents.message_content = True
load_dotenv()



# вікно для реєстрації та редагування інформації
class RegistrationWindow(disnake.ui.Modal):
    def __init__(self, is_edit=False, current_data=None, on_regist=None, on_edit=None):
        self.is_edit = is_edit
        self.current_data = current_data
        self.on_regist = on_regist
        self.on_edit = on_edit

        if is_edit:
            components = [
                disnake.ui.TextInput(
                    label="Ім'я",
                    placeholder="Введіть своє ім'я",
                    custom_id="username",
                    style=TextInputStyle.short,
                    min_length=2,
                    max_length=50,
                    required=False,
                ),
                disnake.ui.TextInput(
                    label="Карта",
                    placeholder="Введіть номер банківської картки",
                    custom_id="bank_card",
                    style=TextInputStyle.short,                
                    min_length=16,
                    max_length=20,
                    required=False,
                ),
            ]
            title = "Редагування інформації"
        else:    
            components = [
                disnake.ui.TextInput(
                    label="Ім'я",
                    placeholder="Введіть своє ім'я",
                    custom_id="username",
                    style=TextInputStyle.short,
                    min_length=2,
                    max_length=50,
                    required=False,
                ),
                disnake.ui.TextInput(
                    label="Карта",
                    placeholder="Введіть номер банківської картки",
                    custom_id="bank_card",
                    style=TextInputStyle.short,                
                    min_length=16,
                    max_length=20,
                    required=False,
                ),
            ]
            title = "Реєстрація"

        super().__init__(title=title, components=components)


    async def callback(self, inter: disnake.ModalInteraction):
        if self.is_edit:
            await self.on_edit(inter)
        else:
            await self.on_regist(inter)



class AdditionalyInfoWindow(disnake.ui.Modal):
    def __init__(self, task_id, task_title, username, bot: commands.Bot):
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
        from ui.buttons import ConfirmCancelTaskBtn
        
        await inter.response.defer()
        get_tasks = GetTasks(self.bot)
        link_to_task = inter.text_values["link"]
        additionaly_description = inter.text_values["additionaly"]
        await update_user_tasks(self.task_id, "Виконується", link_to_task)
        await get_tasks.update_task_info_in_excel(self.task_title, "Виконується", link_to_task)
        
        channel_id = ADMIN_CHANNEL
        channel = self.bot.get_channel(channel_id)

        await channel.send(f"Користувач - {inter.author.name}.\n Виконав завдання - {self.task_title}. \n Опис до завдання: {additionaly_description}", view=ConfirmCancelTaskBtn(self.task_id, inter.author.id, self.task_title, link_to_task, self.bot))
        await inter.followup.send("Завдання надіслано на перевірку! Очікуйте відповідь.")