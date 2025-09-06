import disnake

from disnake import Permissions
from disnake.ext import commands

from config.config import ADMIN_ID, CHANNEL
from cogs.tasks import GetTasks
from services.excel_import import excel_pay_list
from database.requests import add_tasks_into_db, get_all_tasks, clear_tables, get_all_user_to_pay
from ui.buttons import TaskButtons, PayButton
from ui.embeds import tasks_info_embed, pay_info_embed



intents = disnake.Intents.default()
intents.message_content = True



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
            added = await add_tasks_into_db(row['Завдання'], row['Опис завдання'], row['Статус'], row['Пріоритет'], row['Роль'], row['Ціна'], row['Досвід'])
            if added:
                counter += 1
        
        await inter.response.send_message(f"Завдання додано. \n Всього: {counter}")


    # commands for send task into groups
    @commands.slash_command(name="sendtasks", description="надсилає завдання у всі групи", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def send_task(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Розсилка завдань")
        tasks_data = await get_all_tasks()
        
        for tasks in tasks_data:
            if tasks.status not in ["Нове", "Оновлене", "Не розпочато"]:
                continue
            embed = tasks_info_embed(tasks.id, tasks.title, tasks.description, tasks.status, 
                                    tasks.task_priority, tasks.role, tasks.price, tasks.xp)
            channel_id = CHANNEL.get(tasks.role)
            channel = self.bot.get_channel(channel_id)
            
            if not channel_id or not channel:
                print("Not channel!!!")
                continue
            
            await channel.send(embed=embed, view=TaskButtons(self.bot, tasks.id, tasks.title))
    

    @commands.slash_command(name="user_pay", description="список користувачів які мають виплату", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def get_user_pay(self, inter: disnake.ApplicationCommandInteraction):
        result = await get_all_user_to_pay()
        for user_to_pay in result:
            if user_to_pay:
                embed = pay_info_embed(username=user_to_pay.username, bank_card=user_to_pay.user_card, 
                                    amount=user_to_pay.user_balance, task_complated=user_to_pay.user_count_task)
                await inter.send("Користувачі які не отримали виплати: ", embed=embed, view=PayButton(user_to_pay.user_id, 
                                                                                                        amount=user_to_pay.user_balance))


    @commands.slash_command(name="paylist", description="видає список виплат", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def get_pay_list(self, inter: disnake.ApplicationCommandInteraction):
        file_bytes = await excel_pay_list()
        file = disnake.File(file_bytes, filename="payouts.xlsx")
        await inter.response.send_message("Список виплат", file=file)


    # commands for cleat tables data with DB
    @commands.slash_command(name="clear_tables", description="очищає таблиці", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def clear_all_tables(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Таблиці UserTask та Task - очищені")
        await clear_tables()

    
    # clear all chats message
    @commands.slash_command(name="clear_chats", description="очищає всі чати", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def clear_all_chats(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Очищення чатів...")
        for channel in inter.guild.text_channels:
            overwrites = channel.overwrites
            name = channel.name
            category = channel.category
            await inter.guild.create_text_channel(name=name, overwrites=overwrites, category=category)
            await channel.delete()



def setup(bot: commands.Bot):
    bot.add_cog(AdminCmd(bot))
