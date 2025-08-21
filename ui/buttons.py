import disnake

from disnake.ui import Button
from database.database import add_user
from cogs.registration import AssignRoles
from database.requests import add_new_user, edit_user_info, get_user_info
from disnake.ext import commands
from disnake import TextInputStyle
from database.database import update_status_url
from ui.windows import RegistrationWindow
from cogs.reward import Reward

intents = disnake.Intents.default()
intents.message_content = True



# buttons for confirm registration user 
class ConfirmBtn(disnake.ui.View):
    def __init__(self, username: str, bank_card: int, roles: list, user_id: int):
        super().__init__(timeout=300.0)
        self.username = username
        self.bank_card = bank_card
        self.roles = roles
        self.user_id = user_id


    @disnake.ui.button(label="Так", style=disnake.ButtonStyle.grey, emoji="✅")
    async def confirm(self, button: Button, inter: disnake.MessageInteraction):
        try:
            result = await get_user_info(self.user_id)
            if result:
                await edit_user_info(self.user_id, self.username, self.bank_card, self.roles)
                await inter.response.send_message("Дані оновлено успішно!", ephemeral=True)
                assigner = AssignRoles(inter.author, self.roles)
                await assigner.assign_roles()
            else:
                await add_new_user(self.user_id, self.username, self.bank_card, self.roles)    
                assigner = AssignRoles(inter.author, self.roles)
                await assigner.assign_roles()
                await inter.response.send_message("Ви зареєстровані", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Помилка при реєстрації ☣ - {e}. Зв'яжіться з розробником або модератором сервера")


    @disnake.ui.button(label="Ні", style=disnake.ButtonStyle.grey, emoji="❌")
    async def cancel(self, button: Button, inter: disnake.MessageInteraction):
        await inter.response.send_message("Реєстрація скасована", ephemeral=True)



# button - miss step registration
class MissBtn(disnake.ui.View):
    def __init__(self, username: str, bank_card: str, roles: list, user_id: int):
        super().__init__(timeout=300.0)
        self.username = username
        self.bank_card = bank_card
        self.roles = roles
        self.user_id = user_id


    @disnake.ui.button(label="пропустити", style=disnake.ButtonStyle.grey, emoji="➡")
    async def miss(self, button: Button, inter: disnake.MessageInteraction):
        await edit_user_info(self.user_id, self.username, self.bank_card, self.roles)
        await inter.response.send_message("Дані оновлено ✅", ephemeral=True)



# admin btn for confirm or cancel tasks
class ConfirmCancelTaskBtn(disnake.ui.View):
    def __init__(self, task_id, user_id, task_title, link_to_task, bot: commands.Bot):
        self.bot = bot
        self.task_id = task_id
        self.user_id = user_id
        self.link_to_task = link_to_task
        self.task_title = task_title

        super().__init__(timeout=None)
    

    @disnake.ui.button(label="Підтвердити завдання", style=disnake.ButtonStyle.green, custom_id="confirmtasks")
    async def confirm_tasks(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        get_cog = self.bot.get_cog('GetTasks')
        await get_cog.update_task_status_in_excel(self.task_title, "Завершено", self.link_to_task)
        await update_status_url(self.task_id, "Завершено", self.link_to_task)
        user = await self.bot.fetch_user(self.user_id)
        await Reward.reward_user(self.task_id, self.user_id)
        await user.send(f"Ваше завдання було підтверджене - {self.task_title}, бали нараховано")


    @disnake.ui.button(label="Відхилити завдання", style=disnake.ButtonStyle.red, custom_id="canceltasks")
    async def cancel_tasks(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        user = await self.bot.fetch_user(self.user_id)
        await user.send(f"Ваше завдання було відхилене - {self.task_title} Причина: \n", )