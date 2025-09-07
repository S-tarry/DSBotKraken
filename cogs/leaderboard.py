import disnake
from disnake.ext import commands, tasks
from sqlalchemy import select
from database.models import User, assync_session
from config.config import EVENTS_CHANNEL

TOP_EMOJIS = ["🥇", "🥈", "🥉"]



class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message = None
        self.update_leaderboard.start()
        

    @tasks.loop(seconds=60)
    async def update_leaderboard(self):
        # Отримуємо топ-10 користувачів
        async with assync_session() as session:
            users = await session.scalars(select(User).order_by(User.user_level.desc(), User.user_xp.desc()))
            users = users.all()[:10]  # беремо тільки топ-10

        # Формуємо embed
        embed = disnake.Embed(title="🏆 Топ 10 учасників сервера", color=disnake.Color.gold())

        for rank_number, user in enumerate(users, start=1):
            # Додаємо emoji для топ-3, інші просто номер
            if rank_number == 1:
                position = "🥇"
            elif rank_number == 2:
                position = "🥈"
            elif rank_number == 3:
                position = "🥉"
            else:
                position = str(rank_number)

            embed.add_field(
                name=f"{position}. {user.username}",
                value=f"Рівень: {user.user_level}\nРанг: {user.user_rank}",
                inline=False
            )

        # Надсилаємо або редагуємо повідомлення
        channel = self.bot.get_channel(EVENTS_CHANNEL)
        if not self.message:
            self.message = await channel.send(embed=embed)
        else:
            try:
                await self.message.edit(embed=embed)
            except disnake.NotFound:
                self.message = await channel.send(embed=embed)


    @update_leaderboard.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()



def setup(bot: commands.Bot):
    bot.add_cog(Leaderboard(bot))