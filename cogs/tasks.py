import gspread
import disnake

from gspread import Cell
from disnake.ext import commands
from google.oauth2.service_account import Credentials
from config.config import SHEETS_ID


intents = disnake.Intents.default()
intents.message_content = True



# Bot gets tasks
class GetTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # authorization
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("config/credentials.json", scopes=scopes)
        client = gspread.authorize(creds)

        # get data
        sheets_id = SHEETS_ID
        sheet = client.open_by_key(sheets_id)
        self.worksheet = sheet.get_worksheet(0)


    async def load_tasks(self):
        self.values_list = self.worksheet.get_all_records()
    

    # update data in excel
    async def update_task_info_in_excel(self, task_title, status, result_url):
        records = self.worksheet.get_all_records()
        
        for idx, record in enumerate(records, start=2):
            if record['Завдання'] == task_title:
                cell_to_update = [
                    Cell(idx, 3, status),
                    Cell(idx, 8, result_url)
                ]
                self.worksheet.update_cells(cell_to_update)
                break
    


def setup(bot: commands.Bot):
    bot.add_cog(GetTasks(bot))