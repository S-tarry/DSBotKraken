import os
import disnake

from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

# intents = disnake.Intents.default()
# intents.message_content = True

BOT_TOKEN = os.getenv('TOKEN')
SHEETS_ID = os.getenv('SHEETS')

ADMIN_ID = int(os.getenv('ADMIN_ID'))
NOT_REGIST_ID = int(os.getenv('NOT_REGIST_ID'))
REGIST_ID = int(os.getenv('REGIST_ID'))

CHANNEL = {
    'програміст': int(os.getenv('DEVELOPERS')),
    'дизайнер': int(os.getenv('ARTS')),
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



# реєстрація користувача
class Const(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



def setup(bot: commands.Bot):
    bot.add_cog(Const(bot))
