import os
import disnake

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv('TOKEN')
SHEETS_ID = os.getenv('SHEETS')

ADMIN_ID = int(os.getenv('ADMIN_ID'))
NOT_REGIST_ID = int(os.getenv('NOT_REGIST_ID'))
REGIST_ID = int(os.getenv('REGIST_ID'))

CHANNEL = {
    'Програміст': int(os.getenv('DEVELOPERS')),
    'Дизайнер': int(os.getenv('ARTS')),
}
ROLES = {
    # 'не зареєстрований': int(os.getenv('NOTREGIST_ID')),
    'програміст': int(os.getenv('PROGRAMMER_ID')),
    'дизайнер': int(os.getenv('DESIGNER_ID')),
    'тестувальник': int(os.getenv('TESTER_ID')),
}
PRIORITY_COLORS = {
    "Low": disnake.Color.blue(),
    "Medium": disnake.Color.orange(), 
    "High": disnake.Color.red()
}
