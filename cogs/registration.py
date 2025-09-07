import disnake

from disnake.ext import commands
from dotenv import load_dotenv

from database.requests import get_user_info
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
        username = inter.text_values["username"].strip()
        bank_card = inter.text_values["bank_card"].strip()
        await inter.response.send_message("Виберіть роль: ", view=DropdownRoleView(username, bank_card, inter.author.id), ephemeral=True)


    # редагування даних користувача
    async def handle_edit(self, inter: disnake.ModalInteraction):
        from ui.buttons import MissBtn

        user_data = await get_user_info(inter.author.id)
        if not user_data:
            await inter.response.send_message("Ви ще не зареєстровані", ephemeral=True)
            return
    
        current_username = user_data.username
        current_role = [role.name for role in user_data.roles]
        current_card = user_data.user_card

        new_username = inter.text_values["username"].strip() or current_username
        new_bank_card = inter.text_values["bank_card"].strip() or current_card
        new_role = inter.text_values.get("role", "").strip()

        if new_role:
            new_role = [r.strip() for r in new_role.split(",") if r.strip()]
        else:
            new_role = current_role

        if set(new_role) != set(current_role):
            await AssignRoles(inter.author, new_role).update_server_roles() 
        
        await inter.response.send_message("Оновіть свої ролі.", view=DropdownRoleView(new_username, new_bank_card, inter.author.id), ephemeral=True)
        await inter.followup.send("Або пропустіть даний етап за допомогою кнопки.", view=MissBtn(new_username, new_bank_card, new_role, inter.author.id), ephemeral=True)



# надає ролі користувачу --тимчасово, можливе переписання функці--
class AssignRoles():
    def __init__(self, member: disnake.Member, new_roles: list):
        self.member = member
        self.new_roles = new_roles


    async def update_server_roles(self):
        guild = self.member.guild

        roles_to_add = []
        for name in self.new_roles:
            role_id = ROLES.get(name.strip().lower())
            if role_id:
                role = guild.get_role(role_id)
                if role:
                    roles_to_add.append(role)
        
        regist_role = guild.get_role(REGIST_ID)
        roles_to_add.append(regist_role)

        not_regist_role = guild.get_role(NOT_REGIST_ID)
        if not_regist_role in self.member.roles:
            await self.member.remove_roles(not_regist_role)
        
        roles_to_remove = [role for role in self.member.roles if role.id in ROLES.values()]
        if roles_to_remove:
            await self.member.remove_roles(*roles_to_remove)
        
        if roles_to_add:
            await self.member.add_roles(*roles_to_add)



def setup(bot: commands.Bot):
    bot.add_cog(RegistrationUser(bot))
