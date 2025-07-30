import disnake

from disnake.ext import commands
from disnake import TextInputStyle
from database.database import edit_user_info

# -- user info --
# intents = disnake.Intents.default()
# intents.message_content = True
# client = disnake.Client(intents=intents)


class CmdUsers(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # # інформація про користувача
    # @commands.slash_command(name='editinfo', description='редагує інформацію про користувача')
    # async def edit_info(self, inter: disnake.ApplicationCommandInteraction):
    #     await inter.response.send_message("Що ви хочете змінити?",
    #         components=[
    #             disnake.ui.Button(label="Ім'я", style=disnake.ButtonStyle.grey, custom_id="name"),
    #             disnake.ui.Button(label="карта", style=disnake.ButtonStyle.grey, custom_id="card"),
    #             disnake.ui.Button(label="роль", style=disnake.ButtonStyle.grey, custom_id="role"),
    #             disnake.ui.Button(label="все", style=disnake.ButtonStyle.grey, custom_id="all"),
    #         ],
    #     )
    
#     @commands.Cog.listener("on_button_click")
#     async def change_info(self, inter: disnake.MessageInteraction):
#         if inter.component.custom_id not in ["name", "card", "role", "all"]:
#             return
#         if inter.component.custom_id == "name":
#             await inter.response.send_message("Змінення імені користувача")
#         elif inter.component.custom_id == "card":
#             await inter.response.send_message("Змінення карти користувача")
#         elif inter.component.custom_id == "role":
#             await inter.response.send_message("Змінення ролі користувача")
#         elif inter.component.custom_id == "all":
#             await inter.response.send_message("Змінення всіх даних користувача")


# class EditWindow(disnake.ui.Modal):
#     def __init__(self, value):
#         if value == "name":
#             components = [
#                 disnake.ui.TextInput(
#                     label="ім'я",
#                     placeholder="Введіть своє ім'я",
#                     custom_id="username",
#                     style=TextInputStyle.short,
#                     min_length=2,
#                     max_length=50,
#                     required=True,
#                 ),
#             ],
#         elif value == "card":
#             components = [
#                 disnake.ui.TextInput(
#                     label="карта",
#                     placeholder="Введіть номер своєї карти",
#                     custom_id="card",
#                     style=TextInputStyle.short,
#                     min_length=2,
#                     max_length=50,
#                     required=True,
#                 ),
#             ],
#         elif value == "all":
#             components = [
#                 disnake.ui.TextInput(
#                     label="Змінити все",
#                     placeholder="Введіть своє ім'я",
#                     custom_id="username",
#                     style=TextInputStyle.short,
#                     min_length=2,
#                     max_length=50,
#                     required=True,
#                 ),
#                 disnake.ui.TextInput(
#                     label="карта",
#                     placeholder="Введіть номер своєї карти",
#                     custom_id="bank_card",
#                     style=TextInputStyle.short,
#                     min_length=16,
#                     max_length=20,
#                     required=True,
#                 ),
#             ]
#             super().__init__(title="Реєстрація", components=components)





def setup(bot: commands.Bot):
    bot.add_cog(CmdUsers(bot))
