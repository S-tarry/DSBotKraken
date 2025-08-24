# import gspread
# import disnake
# import os

# from google.oauth2.service_account import Credentials
# from disnake import Permissions
# from disnake.ext import commands
# from dotenv import load_dotenv

# from database.database import add_tasks, get_all_tasks, user_tasks, update_status_url, update_all_tasks
# # from disnake import TextInputStyle
# from cogs.config import SHEETS_ID, ADMIN_ID, CHANNEL



# intents = disnake.Intents.default()
# intents.message_content = True
# load_dotenv()




# class GetTasks(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot

#         # авторизація
#         scopes = ["https://www.googleapis.com/auth/spreadsheets"]
#         creds = Credentials.from_service_account_file("services/config/credentials.json", scopes=scopes)
#         client = gspread.authorize(creds)

#         # витяг даних
#         sheets_id = SHEETS_ID
#         sheet = client.open_by_key(sheets_id)
#         self.worksheet = sheet.get_worksheet(0)
#         self.values_list = self.worksheet.get_all_records()
    

#     # оновлення даних в excel
#     async def update_task_status_in_excel(self, task_title, status, result_url):
#         records = self.worksheet.get_all_records()
#         for idx, record in enumerate(records, start=2):
#             if record['Завдання'] == task_title:
#                 self.worksheet.update_cell(idx, 3, status)
#                 self.worksheet.update_cell(idx, 8, result_url)
#                 break