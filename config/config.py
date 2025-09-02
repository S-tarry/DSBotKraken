import os
import disnake


BOT_TOKEN = os.getenv('TOKEN')
SHEETS_ID = os.getenv('SHEETS')

ADMIN_ID = int(os.getenv('ADMIN_ID'))
NOT_REGIST_ID = int(os.getenv('NOT_REGIST_ID'))
REGIST_ID = int(os.getenv('REGIST_ID'))

ADMIN_CHANNEL = int(os.getenv('ADMIN'))
EVENTS_CHANEL = int(os.getenv('EVENTS'))

CHANNEL = {
    'Програміст': int(os.getenv('DEVELOPERS')),
    'Дизайнер': int(os.getenv('ARTS')),
}
ROLES = {
    'програміст': int(os.getenv('PROGRAMMER_ID')),
    'дизайнер': int(os.getenv('DESIGNER_ID')),
    'тестувальник': int(os.getenv('TESTER_ID')),
}
PRIORITY_COLORS = {
    "Low": disnake.Color.blue(),
    "Medium": disnake.Color.orange(), 
    "High": disnake.Color.red()
}
