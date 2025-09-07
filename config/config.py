import os
import disnake

from dotenv import load_dotenv

load_dotenv()

DBPASS = os.getenv('DBPASS')
BOT_TOKEN = os.getenv('TOKEN')

SHEETS_ID = os.getenv('SHEETS')
SERVER_ID = int(os.getenv('SERVER_ID'))

BOT_ID = int(os.getenv('BOT_ID'))
ADMIN_ID = int(os.getenv('ADMIN_ID'))
NOT_REGIST_ID = int(os.getenv('NOT_REGIST_ID'))
REGIST_ID = int(os.getenv('REGIST_ID'))

INFORM_ADMIN_CHANNEL = int(os.getenv('INFORM_FOR_ADMIN'))
EVENTS_CHANNEL = int(os.getenv('EVENTS'))
ADMIN_CHANNEL = int(os.getenv('ADMIN'))
START_CHANNEL = int(os.getenv('START_CHANNEL'))
ERROR_CHANNEL = int(os.getenv('ERROR'))

CHANNEL = {
    'Програміст': int(os.getenv('DEVELOPERS')),
    'Дизайнер': int(os.getenv('ARTS')),
}

RANGS = {
    'новачок': int(os.getenv('NEWBIE'))
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
