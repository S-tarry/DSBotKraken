import disnake

from disnake.ext import commands
# from disnake import TextInputStyle
# from database.database import update_status_url
# from ui.windows import RegistrationWindow
# from cogs.reward import Reward
# import gspread
# import os

# from google.oauth2.service_account import Credentials
from disnake import Permissions
from disnake.ext import commands
# from dotenv import load_dotenv

# from database.database import add_tasks, get_all_tasks, user_tasks, update_status_url, update_all_tasks
from database.requests import add_tasks_into_db, get_all_tasks, clear_tables
# from disnake import TextInputStyle
from config.config import SHEETS_ID, ADMIN_ID, CHANNEL
from ui.buttons import TaskButtons
from cogs.tasks import GetTasks
from ui.embeds import tasks_info_embed
# from disnake.ui import Button



intents = disnake.Intents.default()
intents.message_content = True
# client = disnake.Client(intents=intents)


class AdminCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # commands for add task into DB
    @commands.slash_command(name="addtask", description="додає завдання", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def write_tasks_to_db(self, inter: disnake.ApplicationCommandInteraction):
        """Add all tasks with excel into DB"""
        gettasks: GetTasks = self.bot.get_cog("GetTasks")
        counter = 0
        await gettasks.load_tasks()
        for row in gettasks.values_list:
            await add_tasks_into_db(row['Завдання'], row['Опис завдання'], row['Статус'], row['Пріоритет'], row['Роль'], row['Ціна'], row['Досвід'])
            counter += 1
        
        await inter.response.send_message(f"Завдання додано. \n Всього: {counter}")


    # commands for send task into groups
    @commands.slash_command(name="sendtasks", description="надсилає завдання у всі групи", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def send_task(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Розсилка завдань")
        tasks_data = await get_all_tasks()
        
        for tasks in tasks_data:
            embed = tasks_info_embed(tasks.id, tasks.title, tasks.description, tasks.status, 
                                    tasks.task_priority, tasks.role, tasks.price, tasks.xp)
            channel_id = CHANNEL.get(tasks.role)
            channel = self.bot.get_channel(channel_id)
            
            if not channel_id or not channel:
                print("Not channel!!!")
                continue
            
            await channel.send(embed=embed, view=TaskButtons(self.bot, tasks.id, tasks.title))


    # commands for cleat tables data with DB
    @commands.slash_command(name="clear_tables", description="очищає таблиці", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def clear_all_tables(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Таблиці UserTask та Task - очищені")
        await clear_tables()


        


    #     for task in tasks_data:
    #         task_id, title, description, status, priority, role, total_price, total_xp = task

    #         if status not in ("Нове", "Оновлене", ""):
    #             continue
            
    #         role = role.lower()
    #         channel_id = CHANNEL.get(role)
    #         if not channel_id:
    #             print(f"{channel_id} Немає каналу - {role}")
    #             continue
            
    #         channel = self.bot.get_channel(channel_id)
    #         if not channel:
    #             print(f"Невказано id для каналу в коді - {role}")
    #             continue
            
    #         priority_colors = {
    #             "Low": disnake.Color.blue(),
    #             "Medium": disnake.Color.orange(), 
    #             "High": disnake.Color.red()
    #         }

    #         embed = disnake.Embed(
    #             title=f"{title}",
    #             description=f"{description}",
    #             color=priority_colors.get(priority, disnake.Color.greyple())
    #         )
    #         embed.add_field(name="Пріоритет", value=priority, inline=False)
    #         embed.add_field(name="Ціна", value=total_price, inline=True)
    #         embed.add_field(name="Досвід", value=total_xp, inline=True)

            # await channel.send(embed=embed, view=TaskButtons(task_id, title, self))
    #         await update_all_tasks(title, description, priority, total_price, total_xp, task_id)
    #         await update_status_url(task_id, "Не розпочато", None)
    #         await self.update_task_status_in_excel(title, "Не розпочато", None)

    #         print("Надіслано та оновлено")

    #     await inter.followup.send("Завдання надіслані успішно")


# # кнопки для відправки завдань на перевірку та відхилення
# class AdminTasksBtn(disnake.ui.View):
#     def __init__(self, task_id, user_id, task_title, link_to_task, bot: commands.Bot):
#         self.bot = bot
#         self.task_id = task_id
#         self.user_id = user_id
#         self.link_to_task = link_to_task
#         self.task_title = task_title

#         super().__init__(timeout=None)
    

#     @disnake.ui.button(label="Підтвердити завдання", style=disnake.ButtonStyle.green, custom_id="confirmtasks")
#     async def confirm_tasks(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
#         get_cog = self.bot.get_cog('GetTasks')
#         await get_cog.update_task_status_in_excel(self.task_title, "Завершено", self.link_to_task)
#         await update_status_url(self.task_id, "Завершено", self.link_to_task)
#         user = await self.bot.fetch_user(self.user_id)
#         await Reward.reward_user(self.task_id, self.user_id)
#         await user.send(f"Ваше завдання було підтверджене - {self.task_title}, бали нараховано")


#     @disnake.ui.button(label="Відхилити завдання", style=disnake.ButtonStyle.red, custom_id="canceltasks")
#     async def cancel_tasks(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
#         user = await self.bot.fetch_user(self.user_id)
#         await user.send(f"Ваше завдання було відхилене - {self.task_title} Причина: \n", )


def setup(bot: commands.Bot):
    bot.add_cog(AdminCmd(bot))
