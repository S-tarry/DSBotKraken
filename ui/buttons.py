import disnake

from disnake.ui import Button
from cogs.registration import AssignRoles
from database.requests import add_new_user, edit_user_info, get_user_info, add_user_tasks, update_user_tasks, add_payout_info, update_user_info
from disnake.ext import commands
from ui.windows import AdditionalyInfoWindow, ReasonCancelTasks
from economy.reward import reward_user
from cogs.tasks import GetTasks


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
                await AssignRoles(inter.author, self.roles).update_server_roles()
            else:
                await add_new_user(self.user_id, self.username, self.bank_card, self.roles)    
                await AssignRoles(inter.author, self.roles).update_server_roles()
                await inter.response.send_message("Ви зареєстровані", ephemeral=True)
        except Exception as e:
            print(f"Помилка при реєстрації ☣ - {e}. Зв'яжіться з розробником або модератором сервера")
            await inter.send(f"Помилка при реєстрації ☣ - {e}. Зв'яжіться з розробником або модератором сервера", ephemeral=True)


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



# buttons for user - take tasks
class TaskButtons(disnake.ui.View):
    def __init__(self, bot: commands.Bot, task_id, task_title):
        self.bot = bot
        self.task_id = task_id
        self.task_title = task_title
        super().__init__(timeout=None)


    @disnake.ui.button(label="Прийняти", style=disnake.ButtonStyle.green, custom_id="confirm")
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message(f"Завдання - {self.task_title}, було взяте.")
        await inter.message.delete()
        await add_user_tasks(inter.author.id, self.task_id)
        await update_user_tasks(self.task_id, "Виконується", "")
        get_tasks = GetTasks(self.bot)
        await get_tasks.update_task_info_in_excel(self.task_title, "Виконується", "")


# buttons how send messages into admin
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
        # await inter.response.edit_message(content="завдання відправлено на перевірку", view=None)


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
        get_tasks = GetTasks(self.bot)
        await reward_user(self.user_id, self.task_id, self.bot)
        await get_tasks.update_task_info_in_excel(self.task_title, "Завершено", self.link_to_task)
        await update_user_tasks(self.task_id, "Завершено", self.link_to_task)
        await update_user_info(self.user_id)
        await inter.message.delete()
        user = await self.bot.fetch_user(self.user_id)
        await user.send(f"Ваше завдання було підтверджене - {self.task_title}")


    @disnake.ui.button(label="Відхилити завдання", style=disnake.ButtonStyle.red, custom_id="canceltasks")
    async def cancel_tasks(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        modal = ReasonCancelTasks(self.bot, self.user_id, self.task_title)
        await inter.response.send_modal(modal)



class PayButton(disnake.ui.View):
    def __init__(self, user_id: int, amount: int):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.amount = amount


    @disnake.ui.button(label="Виплатити", style=disnake.ButtonStyle.green, custom_id="pay")
    async def pay_out(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await add_payout_info(self.user_id, self.amount)
        await inter.response.send_message("Виплата здійснена успішно")