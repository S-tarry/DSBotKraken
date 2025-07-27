import disnake
from disnake.ext import commands

# from database.database import init_db

# -- user info --
# intents = disnake.Intents.default()
# intents.message_content = True
# client = disnake.Client(intents=intents)


class CmdUsers(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # перший запуск бота
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     await init_db()
    #     print("Привіт, я бот - KrakenGAmmers")

    # просто тест
    # @commands.slash_command(name='register', description='реєструє користувача')
    # async def profile(self, inter: disnake.ApplicationCommandInteraction):
    #     await inter.response.send_message("Hello. You using COGS")

    # інформація про користувача
    @commands.slash_command(name='myinfo', description='sdcl,s')
    async def my_info(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title="Panel info ",
            color=disnake.Colour.yellow(),
        )
        embed.set_author(
            name=f"Your nickname: {inter.author.name}",
        )
        embed.add_field(name="Your money", value="122", inline=False)
        # await inter.response.send_message(embed=embed)
        await inter.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CmdUsers(bot))
