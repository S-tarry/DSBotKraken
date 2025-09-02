import disnake

from dotenv import load_dotenv
from disnake.ext import commands
from database.requests import get_user_info, add_all_roles_into_db
from config.config import ROLES, REGIST_ID, NOT_REGIST_ID
from ui.select_menu import DropdownRoleView


intents = disnake.Intents.default()
intents.message_content = True
load_dotenv()



# реєстрація користувача
class RegistrationUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # реєcтрація користувача
    async def handle_regist(self, inter: disnake.ModalInteraction):
        guild = self.bot.get_guild(1394340735821811712)
        roles_id_to_skip = [1404536880623521925, 1394344787435585660]
        await add_all_roles_into_db(guild.roles, roles_id_to_skip)


        username = inter.text_values["username"].strip()
        bank_card = inter.text_values["bank_card"].strip()
        await inter.response.send_message("Виберіть роль: ", view=DropdownRoleView(username, bank_card, inter.author.id), ephemeral=True)


    # редагування даних користувача
    async def handle_edit(self, inter: disnake.ModalInteraction):
        from ui.buttons import MissBtn

        user_data = await get_user_info(inter.author.id)
        if not user_data:
            await inter.response.send_message("Ви не зареєстровані", ephemeral=True)
            return
    
        current_username = user_data.username
        current_role = [role.name for role in user_data.roles]
        current_card = user_data.user_card
        print(current_role)

        new_username = inter.text_values["username"].strip() or current_username
        new_bank_card = inter.text_values["bank_card"].strip() or current_card
        new_role = inter.text_values.get("role", "").strip()
        print("New Roles: ", new_role)

        if new_role:
            new_role = [r.strip() for r in new_role.split(",") if r.strip()]
        else:
            new_role = current_role

        if set(new_role) != set(current_role):
            await self.update_server_roles(inter, new_role) 
        
        await inter.response.send_message("Оновіть свої ролі: ", view=DropdownRoleView(new_username, new_bank_card, inter.author.id), ephemeral=True)
        await inter.followup.send("Або пропустіть даний етап за допомогою кнопки - ", view=MissBtn(new_username, new_bank_card, new_role, inter.author.id))


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

        regist_role = self.member.guild.get_role(REGIST_ID)
        if regist_role:
            roles_to_add.append(regist_role)

        not_reg_role = self.member.guild.get_role(NOT_REGIST_ID)
        if not_reg_role and not_reg_role in self.member.roles:
            await self.member.remove_roles(not_reg_role)

        if roles_to_add:
            await self.member.add_roles(*roles_to_add)
            print("Roles add: ", roles_to_add)



def setup(bot: commands.Bot):
    bot.add_cog(RegistrationUser(bot))
