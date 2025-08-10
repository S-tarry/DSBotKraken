import disnake

from disnake.ext import commands
from disnake import TextInputStyle
from database.database import update_status_url
from cogs.registration import RegistrationWindow
from cogs.reward import Reward
# from disnake.ui import Button



intents = disnake.Intents.default()
intents.message_content = True
# client = disnake.Client(intents=intents)


class AdminCmd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


# кнопки для відправки завдань на перевірку та відхилення
class AdminTasksBtn(disnake.ui.View):
    def __init__(self, task_id, user_id, task_title, link_to_task, bot: commands.Bot):
        self.bot = bot
        self.task_id = task_id
        self.user_id = user_id
        self.link_to_task = link_to_task
        self.task_title = task_title

        super().__init__(timeout=None)
    
    @disnake.ui.button(label="Підтвердити завдання", style=disnake.ButtonStyle.green, custom_id="confirmtasks")
    async def confirm_tasks(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        get_cog = self.bot.get_cog('GetTasks')
        await get_cog.update_task_status_in_excel(self.task_title, "Завершено", self.link_to_task)
        await update_status_url(self.task_id, "Завершено", self.link_to_task)
        user = await self.bot.fetch_user(self.user_id)
    
        await Reward.reward_user(self.task_id, self.user_id)
        
        await user.send(f"Ваше завдання було підтверджене - {self.task_title}, бали нараховано")

    @disnake.ui.button(label="Відхилити завдання", style=disnake.ButtonStyle.red, custom_id="canceltasks")
    async def cancel_tasks(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        user = await self.bot.fetch_user(self.user_id)
        await user.send(f"Ваше завдання було відхилене - {self.task_title} Причина: \n", )


def setup(bot: commands.Bot):
    bot.add_cog(AdminCmd(bot))
