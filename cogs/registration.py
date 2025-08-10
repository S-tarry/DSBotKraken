import disnake
import os

from disnake.ext import commands
from disnake.ui import Select, View
from disnake import TextInputStyle

from dotenv import load_dotenv
from database.database import get_user_info, edit_user_info
from cogs.const import ROLES

intents = disnake.Intents.default()
intents.message_content = True
load_dotenv()

# ROLES = {
#     'не зареєстрований': int(os.getenv('NOTREGIST_ID')),
#     'програміст': int(os.getenv('PROGRAMMER_ID')),
#     'дизайнер': int(os.getenv('DESIGNER_ID')),
#     'тестувальник': int(os.getenv('TESTER_ID')),
# }



# реєстрація користувача
class RegistrationUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 

# вікно реєстрації
class RegistrationWindow(disnake.ui.Modal):
    def __init__(self, is_edit=False, current_data=None):
        self.is_edit = is_edit
        self.current_data = current_data
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
            await self.handle_edit(inter)
        else:
            await self.handle_regist(inter)
    
    # реєcтрація користувача
    async def handle_regist(self, inter: disnake.ModalInteraction):
        username = inter.text_values["username"].strip()
        bank_card = inter.text_values["bank_card"].strip()
        await inter.response.send_message("Виберіть роль: ", view=DropdownRoleView(username, bank_card, inter.author.id), ephemeral=True)

    # редагування даних користувача
    async def handle_edit(self, inter: disnake.ModalInteraction):
        user_data = await get_user_info(inter.author.id)
        if not user_data:
            await inter.response.send_message("Ви не зареєстровані", ephemeral=True)
            return
    
        current_username = user_data[1]
        current_role = user_data[2]
        current_card = user_data[3]

        new_username = inter.text_values["username"].strip() if inter.text_values["username"].strip() else current_username
        new_role = inter.text_values["role"].strip().lower() if inter.text_values["role"].strip().lower() else current_role
        new_bank_card = inter.text_values["bank_card"].strip()if inter.text_values["bank_card"].strip() else current_card
        
        # -------------------можливе переписання-------------------
        valid_roles = []
        invalid_roles = []
        for role_name in new_role.split(","):
            role_name = role_name.strip().lower()
            if role_name in ROLES:
                valid_roles.append(role_name)
            else:
                invalid_roles.append(role_name)
        if invalid_roles:
            await inter.response.send_message(f"❌ Ці ролі не знайдено: {', '.join(invalid_roles)} \n Спробуйте ще раз", ephemeral=True)
            return
        # ---------------------------------------------------------
        await edit_user_info(new_username, new_role, new_bank_card, inter.author.id)

        if new_role != current_role:
            await self.update_server_roles(inter, new_role.split(", "))        
        await inter.response.send_message("Дані були успішно оновленні", ephemeral=True)

    
    # оновлення ролі на сервері
    async def update_server_roles(self, inter: disnake.ModalInteraction, new_roles):
        # -------------------можливе переписання-------------------
        member = inter.author
        roles_to_remove = []
        for role in member.roles:
            if role.id in ROLES.values():
                roles_to_remove.append(role)
        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)
        
        roles_to_add = []
        for role_name in new_roles:
            role_id = ROLES.get(role_name.strip().lower())
            if role_id:
                role = member.guild.get_role(role_id)
                if role:
                    roles_to_add.append(role)
        if roles_to_add:
            await member.add_roles(*roles_to_add)
        # ---------------------------------------------------------



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
        from cogs.buttons import ConfirmBtn
        
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



# надає ролі користувачу --тимчасово, можливе переписання функці--
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
# class ConfirmBtn(disnake.ui.View):
#     def __init__(self, username: str, bank_card: int, roles: list, user_id: int):
#         super().__init__(timeout=300.0)
#         self.username = username
#         self.bank_card = bank_card
#         self.roles = roles
#         self.user_id = user_id


#     @disnake.ui.button(label="Так", style=disnake.ButtonStyle.green, emoji="✅")
#     async def confirm(self, button: Button, inter: disnake.MessageInteraction):
#         try:
#             roles_str = ", ".join(self.roles)
#             await add_user(user_id=self.user_id, username=self.username, role=roles_str, bank_card=self.bank_card)
#             view = AssignRoles(inter.author, self.roles)
#             await view.assign_roles()
#             await inter.response.send_message("Ви зареєстровані")
#         except Exception as e:
#             await inter.response.send_message("Помилка при реєстрації")

#     @disnake.ui.button(label="Ні", style=disnake.ButtonStyle.red, emoji="❌")
#     async def cancel(self, button: Button, inter: disnake.CommandInteraction):
#         await inter.response.send_message("Реєстрація скаксована") 


def setup(bot: commands.Bot):
    bot.add_cog(RegistrationUser(bot))
