import disnake
from disnake.ext import commands, tasks


intents = disnake.Intents.default()
intents.message_content = True
client = disnake.Client(intents=intents)



class Main(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    
    


    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        channel = disnake.utils.get(member.guild.text_channels, name="чат")
        if channel:
            await channel.send("Привіт, я бот Kraken Gamers призначений для покращення комунікації... Спочатку вам потрібно пройти реєстрацію для цього використовуйте команду /register")

    

def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))
