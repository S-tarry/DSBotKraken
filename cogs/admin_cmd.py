import disnake
import traceback

from disnake import Permissions
from disnake.ext import commands

from utils.error_handler import logger, send_error_or_info
from config.config import ADMIN_ID, CHANNEL, INFORM_ADMIN_CHANNEL, ERROR_CHANNEL
from cogs.tasks import GetTasks
from services.excel_import import excel_pay_list
from database.requests import add_tasks_into_db, get_all_tasks, clear_tables, get_all_user_to_pay
from ui.buttons import TaskButtons, PayButton
from ui.embeds import tasks_info_embed, pay_info_embed



class AdminCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # commands for add task into DB
    @commands.slash_command(name="add_task", description="додає завдання в БД", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def write_tasks_to_db(self, inter: disnake.ApplicationCommandInteraction):
        try:
            gettasks: GetTasks = self.bot.get_cog("GetTasks")
            counter = 0
            await gettasks.load_tasks()

            for row in gettasks.values_list:
                await add_tasks_into_db(row['Завдання'], row['Опис завдання'], row['Статус'], row['Пріоритет'], row['Роль'], row['Ціна'], row['Досвід'])
                counter += 1
            
            await inter.response.send_message(f"Завдання додано!\nВсього: {counter} завдань.")
        except Exception as e:
            await send_error_or_info(self.bot, "Виникла помилка при додаванні завдання.", ERROR_CHANNEL)
            logger.error(f"Помилка при додаванні завдання. {e}\n{traceback.format_exc()}")


    # commands for send task into groups
    @commands.slash_command(name="send_tasks", description="надсилає завдання у всі групи", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def send_task(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Розсилка завдань...")
        tasks_data = await get_all_tasks()
        
        for tasks in tasks_data:
            try:
                if tasks.status not in ["Нове", "Оновлене", "Не розпочато"]:
                    continue
                embed = tasks_info_embed(tasks.id, tasks.title, tasks.description, tasks.status, 
                                        tasks.task_priority, tasks.role, tasks.price, tasks.xp)
                channel_id = CHANNEL.get(tasks.role)
                channel = self.bot.get_channel(channel_id)
                
                if not channel_id or not channel:
                    continue
                
                await channel.send(embed=embed, view=TaskButtons(self.bot, tasks.id, tasks.title))
            except Exception as e:
                await send_error_or_info(self.bot, f"Завдання - {tasks.title}, не надіслано!", ERROR_CHANNEL)
                logger.error(f"Помилка при надсиланні завданнь. {e}\n{traceback.format_exc()}")
    

    @commands.slash_command(name="user_pay", description="видає список виплат для користувачів", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def get_user_pay(self, inter: disnake.ApplicationCommandInteraction):
        result = await get_all_user_to_pay()
        try:
            for user_to_pay in result:
                if user_to_pay:
                    embed = pay_info_embed(username=user_to_pay.username, bank_card=user_to_pay.user_card, 
                                        amount=user_to_pay.user_balance, task_complated=user_to_pay.user_count_task)
                    await inter.send("Користувачі які не отримали виплати: ", embed=embed, view=PayButton(user_to_pay.user_id, 
                                                                                                            amount=user_to_pay.user_balance))
        except Exception as e:
            await send_error_or_info(self.bot, "Виникла помилка при отримані списку з користувачами які мають виплату.", ERROR_CHANNEL)
            logger.error(f"Помилка при при отриманні оплати користувачів. {e}\n{traceback.format_exc()}")


    @commands.slash_command(name="list_pay", description="формує файл з виплатами", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def get_pay_list(self, inter: disnake.ApplicationCommandInteraction):
        try:
            file_bytes = await excel_pay_list()
            file = disnake.File(file_bytes, filename="payouts.xlsx")
            await send_error_or_info(self.bot, "📜Список виплат", INFORM_ADMIN_CHANNEL, file=file)
        except Exception as e:
            await send_error_or_info(self.bot, "Виникла помилка при формуванні списку виплат.", ERROR_CHANNEL)
            logger.error(f"Помилка при формуванні списку виплат. {e}\n{traceback.format_exc()}")


    # commands for cleat tables data with DB
    @commands.slash_command(name="tables_clear", description="очищає таблиці в БД", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def clear_all_tables(self, inter: disnake.ApplicationCommandInteraction):
        try:
            await send_error_or_info(self.bot, "Таблиці UserTask, Task, Payout - очищені.", INFORM_ADMIN_CHANNEL)
            await clear_tables()
        except Exception as e:
            await send_error_or_info(self.bot, "Виникла помилка при очищенні таблиць в БД.", ERROR_CHANNEL)
            logger.error(f"Помилка при формуванні списку виплат. {e}\n{traceback.format_exc()}")

    
    # clear all chats message
    @commands.slash_command(name="chats_clear", description="очищає всі чати", default_member_permissions=Permissions(manage_guild=True))
    @commands.has_role(ADMIN_ID)
    async def clear_all_chats(self, inter: disnake.ApplicationCommandInteraction):
        await send_error_or_info(self.bot, "Чати очищенні", INFORM_ADMIN_CHANNEL)
        for channel in inter.guild.text_channels:
            try:
                await channel.purge(limit=None)
                await channel.send("Чат очищено", delete_after=3)
            except Exception as e:
                await send_error_or_info(self.bot, "Виникла помилка при очищенні чатів.", ERROR_CHANNEL)
                logger.error(f"Помилка при очищенні чатів. {e}\n{traceback.format_exc()}")



def setup(bot: commands.Bot):
    bot.add_cog(AdminCmd(bot))
