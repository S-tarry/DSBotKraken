import disnake

from disnake.ext import commands
from disnake.ui import Button
from database.database import add_user
from cogs.registration import AssignRoles

intents = disnake.Intents.default()
intents.message_content = True



# службові кнопки
class ServiceButtons(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



# кнопки для підтвердження реєстрації користувача 
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
            roles_str = ", ".join(self.roles)
            await add_user(self.user_id, self.username, roles_str, self.bank_card)
            view = AssignRoles(inter.author, self.roles)
            await view.assign_roles()
            await inter.response.send_message("Ви зареєстровані", ephemeral=True)
        except Exception as e:
            await inter.response.send_message("Помилка при реєстрації", ephemeral=True)

    @disnake.ui.button(label="Ні", style=disnake.ButtonStyle.grey, emoji="❌")
    async def cancel(self, button: Button, inter: disnake.MessageInteraction):
        await inter.response.send_message("Реєстрація скаксована", ephemeral=True) 



def setup(bot: commands.Bot):
    bot.add_cog(ServiceButtons(bot))
