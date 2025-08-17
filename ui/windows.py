import disnake
import os

from disnake.ext import commands
from disnake.ui import Select, View
from disnake import TextInputStyle

from dotenv import load_dotenv
from database.database import get_user_info, edit_user_info
from cogs.config import ROLES, REGIST_ID, NOT_REGIST_ID

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
                disnake.ui.TextInput(
                    label="Роль",
                    placeholder="Вкажіть роль/ролі через кому",
                    custom_id="role",
                    style=TextInputStyle.short,                
                    min_length=3,
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