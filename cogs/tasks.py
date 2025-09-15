import asyncio
import gspread
import gspread_asyncio

from disnake.ext import commands
from gspread import Cell
from google.oauth2.service_account import Credentials

from config.config import SHEETS_ID



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
        # self.values_list = self.worksheet.get_all_records()
        self.values_list = await asyncio.to_thread(self.worksheet.get_all_records)
    

    # update data in excel
    async def update_task_info_in_excel(self, task_title, status, result_url):
        records = await asyncio.to_thread(self.worksheet.get_all_records)
        cells_to_update = []
        # records = self.worksheet.get_all_records()
        # cells_to_update = []
        # cell = self.worksheet.find(task_title, in_column=1)
        # if cell:
        #     self.worksheet.update_cells([
        #         Cell(cell.row, 3, status),
        #         Cell(cell.row, 8, result_url)
        #     ])
        for idx, record in enumerate(records, start=2):
            if record['Завдання'] == task_title:
                cells_to_update.extend([
                    Cell(idx, 3, status),
                    Cell(idx, 8, result_url)
                ])
                break
        if cells_to_update:
            await asyncio.to_thread(self.worksheet.update_cells, cells_to_update)
        # for idx, record in enumerate(records, start=2):
        #     if record['Завдання'] == task_title:
        #         cell_to_update = [
        #             Cell(idx, 3, status),
        #             Cell(idx, 8, result_url)
        #         ]
        #         self.worksheet.update_cells(cell_to_update)
        #         break
    


def setup(bot: commands.Bot):
    bot.add_cog(GetTasks(bot))