import disnake
from disnake.ext import commands


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
    
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author == client.user:
    #         return 
    @commands.slash_command(description="вибір ролі")
    async def roles(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send("Виберіть роль: ", view=DropdownRoleView())
    # @commands.command()
    # async def roles(self, inter: disnake.ApplicationCommandInteraction):
        # await inter.send("Виберіть роль: ", view=DropdownRoleView())


class DropdownRoleMenu(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label="програміст", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="програміст1", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="програміст2", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="програміст3", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="програміст4", description="написання коду", emoji="👨🏽‍💻"),
        ]

        super().__init__(
            placeholder="Вибери роль/ролі",
            min_values=1,
            max_values=3,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.send_message(f"Ваші ролі: {self.values}")
    
    
class DropdownRoleView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownRoleMenu())
    # @commands.Cog.listener()
    # async def on_member_join(self, member: disnake.Member):
    #     role = await disnake.utils.get(guild_id=member.guild.id,
    #                                    role_id=1396543468783800393)
    #     channel = member.guild.system_channel
    #     await member.add_roles(role)
    #     if channel is not None:
    #         await channel.send(f'Welcome {member.mention}.')
    

def setup(bot: commands.Bot):
    bot.add_cog(Main(bot))
