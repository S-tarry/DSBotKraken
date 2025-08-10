import disnake
import os

from disnake.ext import commands

from dotenv import load_dotenv


intents = disnake.Intents.default()
intents.message_content = True
load_dotenv()

SHEETS_ID = os.getenv('SHEETS')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL = {
    'програміст': int(os.getenv('DEVELOPERS')),
    'дизайнер': int(os.getenv('ARTS')),
}
ROLES = {
    'не зареєстрований': int(os.getenv('NOTREGIST_ID')),
    'програміст': int(os.getenv('PROGRAMMER_ID')),
    'дизайнер': int(os.getenv('DESIGNER_ID')),
    'тестувальник': int(os.getenv('TESTER_ID')),
}



# реєстрація користувача
class Const(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



def setup(bot: commands.Bot):
    bot.add_cog(Const(bot))
