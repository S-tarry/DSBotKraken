import disnake
import os

from dotenv import load_dotenv
from disnake.ext import commands
from disnake.ui import Button, Select, View
from disnake import TextInputStyle
from database.database import add_user, get_user_info, edit_user_info

intents = disnake.Intents.default()
intents.message_content = True
load_dotenv()

ROLES = {
    'не зареєстрований': int(os.getenv('NOTREGIST_ID')),
    'програміст': int(os.getenv('PROGRAMMER_ID')),
    'дизайнер': int(os.getenv('DESIGNER_ID')),
    'тестувальник': int(os.getenv('TESTER_ID')),
}



# реєстрація користувача
class RegistrationUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # команда - regist
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


# вікно реєстрації
class RegistrationWindow(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Ім'я",
                placeholder="Введіть своє ім'я",
                custom_id="username",
                style=TextInputStyle.short,
                min_length=2,
                max_length=50,
                required=True,
            ),
            disnake.ui.TextInput(
                label="Карта",
                placeholder="Введіть номер банківської картки",
                custom_id="bank_card",
                style=TextInputStyle.short,                
                min_length=16,
                max_length=20,
                required=True,
            ),
        ]
        super().__init__(title="Реєстрація", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        username = inter.text_values["username"].strip()
        bank_card = inter.text_values["bank_card"].strip()
        await inter.response.send_message("Виберіть роль: ", view=DropdownRoleView(username, bank_card, inter.author.id), ephemeral=True)


# випадаючий список з ролями
class DropdownRoleMenu(Select):
    def __init__(self, username: str, bank_card: int, user_id: int):
        self.username = username
        self.bank_card = bank_card
        self.user_id = user_id

        options = [
            disnake.SelectOption(label="програміст", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="дизайнер", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="тестувальник", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="програміст3", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="програміст4", description="написання коду", emoji="👨🏽‍💻"),
        ]

        super().__init__(
            placeholder="Вибери роль/ролі",
            min_values=1,
            max_values=3,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.defer()
        view = ConfirmBtn(self.username, self.bank_card, self.values, self.user_id)
        roles_text = ", ".join(self.values)
        embed = disnake.Embed(
            title="Підтвердити інформацію?",
            color=disnake.Color.blue()
        )
        embed.add_field(name="Ім'я", value=self.username, inline=False)
        embed.add_field(name="Картка", value=self.bank_card, inline=False)
        embed.add_field(name="Ролі", value=roles_text, inline=False)
        await inter.followup.send(embed=embed, view=view, ephemeral=True)


# перегляд списку з ролями    
class DropdownRoleView(View):
    def __init__(self, username: str, bank_card: int, user_id: int):
        super().__init__(timeout=300.0)
        self.add_item(DropdownRoleMenu(username, bank_card, user_id))
    

# надає ролі користувачу --тимчасово--
class AssignRoles():
    def __init__(self, member: disnake.Member, roles: list):
        self.member = member
        self.roles = roles

    async def assign_roles(self):
        roles_to_add = []
        for role_name in self.roles:
            role_id = ROLES.get(role_name.strip().lower())
            if role_id:   
                role = self.member.guild.get_role(role_id)
                if role:
                    roles_to_add.append(role)
        if roles_to_add:
            await self.member.add_roles(*roles_to_add)
            print("Roles add: ", roles_to_add)


# кнопки підтвердження та відхилення 
class ConfirmBtn(disnake.ui.View):
    def __init__(self, username: str, bank_card: int, roles: list, user_id: int):
        super().__init__(timeout=300.0)
        self.username = username
        self.bank_card = bank_card
        self.roles = roles
        self.user_id = user_id


    @disnake.ui.button(label="Так", style=disnake.ButtonStyle.green, emoji="✅")
    async def confirm(self, button: Button, inter: disnake.MessageInteraction):
        try:
            roles_str = ", ".join(self.roles)
            await add_user(user_id=self.user_id, username=self.username, role=roles_str, bank_card=self.bank_card)
            view = AssignRoles(inter.author, self.roles)
            await view.assign_roles()
            await inter.response.send_message("Ви зареєстровані")
        except Exception as e:
            await inter.response.send_message("Помилка при реєстрації")

    @disnake.ui.button(label="Ні", style=disnake.ButtonStyle.red, emoji="❌")
    async def cancel(self, button: Button, inter: disnake.CommandInteraction):
        await inter.response.send_message("Реєстрація скаксована") 


def setup(bot: commands.Bot):
    bot.add_cog(RegistrationUser(bot))
