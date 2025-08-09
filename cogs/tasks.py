import gspread
from google.oauth2.service_account import Credentials
import disnake
import os

from dotenv import load_dotenv
from disnake.ext import commands
from database.database import add_tasks, get_all_tasks, user_tasks, update_status, update_all_tasks



intents = disnake.Intents.default()
intents.message_content = True
load_dotenv()
SHEETS_ID = os.getenv('SHEETS')
CHANNEL = {
    'Програміст': int(os.getenv('DEVELOPERS')),
    'Дизайнер': int(os.getenv('ARTS')),
}


# Бот отримує завдання
class GetTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # аворизація
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("cogs/config/credentials.json", scopes=scopes)
        client = gspread.authorize(creds)

        # витяг даних
        sheets_id = SHEETS_ID
        sheet = client.open_by_key(sheets_id)
        self.worksheet = sheet.get_worksheet(0)
        self.values_list = self.worksheet.get_all_records()
        # print(values_list)
    
    async def update_task_status_in_excel(self, task_title, status):
        records = self.worksheet.get_all_records()
        for idx, record in enumerate(records, start=2):
            if record['Завдання'] == task_title:
                self.worksheet.update_cell(idx, 3, status)
                break

    @commands.slash_command(name="add_task", description="додає завдання")
    async def write_tasks_to_db(self, inter: disnake.ApplicationCommandInteraction):
        counter = 0
        for row in self.values_list:
            await add_tasks(row['Завдання'], row['Опис завдання'], row['Статус'], row['Пріоритет'], row['Роль'], row['Ціна'], row['Досвід'])
            counter += 1
        await inter.response.send_message(f"Завдання додано \n Всього: {counter}")

    @commands.slash_command(name="send_tasks", description="надсилає завдання у всі групи")
    async def send_task(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Розсилка завдань")
        tasks_data = await get_all_tasks()

        for task in tasks_data:
            task_id, title, description, status, priority, role, total_price, total_xp = task

            if status not in ("Нове", "Оновлене", ""):
                continue
                
            channel_id = CHANNEL.get(role)
            if not channel_id:
                print(f"Немає каналу - {role}")
                continue
            
            channel = self.bot.get_channel(channel_id)
            if not channel:
                print(f"Невказано id для каналу в коді - {role}")
                continue
            
            priority_colors = {
                "Low": disnake.Color.blue(),
                "Medium": disnake.Color.orange(), 
                "High": disnake.Color.red()
            }

            embed = disnake.Embed(
                title=f"{title}",
                description=f"{description}",
                color=priority_colors.get(priority, disnake.Color.greyple())
            )
            embed.add_field(name="Пріоритет", value=priority, inline=False)
            embed.add_field(name="Ціна", value=total_price, inline=True)
            embed.add_field(name="Досвід", value=total_xp, inline=True)

            await channel.send(embed=embed, view=TaskButtons(task_id, title, self))
            await update_all_tasks(title, description, priority, total_price, total_xp, task_id)
            await update_status(task_id, "Не розпочато")
            await self.update_task_status_in_excel(title, "Не розпочато")

            print("Надіслано та оновлено")

            # await channel.send(embed=embed, view=TaskButtons(task_id, title, self))
        await inter.followup.send("Завдання надіслані успішно")


# кнопки для взяття завдань
class TaskButtons(disnake.ui.View):
    def __init__(self, task_id, task_title, cog: GetTasks):
        self.task_id = task_id
        self.task_title = task_title
        self.cog = cog

        super().__init__(timeout=None)

    @disnake.ui.button(label="Прийняти", style=disnake.ButtonStyle.green, custom_id="confirm")
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await user_tasks(inter.author.id, self.task_id, "Виконується", None)
        await update_status(self.task_id, "Виконується")
        await self.cog.update_task_status_in_excel(self.task_title, "Виконується")
        await inter.response.send_message(f"Ви взяли завдання - {self.task_title}")
        await inter.message.delete()
    

def setup(bot: commands.Bot):
    bot.add_cog(GetTasks(bot))