import disnake
from disnake.ext import commands, tasks
from database.requests import add_all_roles_into_db
from config.config import ADMIN_ID, SERVER_ID, NOT_REGIST_ID, START_CHANNEL


intents = disnake.Intents.default()
intents.message_content = True
client = disnake.Client(intents=intents)



class Main(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(SERVER_ID)
        if guild:
            await add_all_roles_into_db(guild.roles, [ADMIN_ID])
            print("All roles add into db")


    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        role = member.guild.get_role(NOT_REGIST_ID)
        if role:
            await member.add_roles(role)
        channel = self.bot.get_channel(START_CHANNEL)
        if channel:
            await channel.send("Привіт, я бот Kraken Gamers призначений для покращення комунікації... Спочатку вам потрібно пройти реєстрацію для цього використовуйте команду /regist")

    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role: disnake.Role):
        await add_all_roles_into_db([role], [ADMIN_ID])
        print(f"New role - {role.name} add to db")



def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))
