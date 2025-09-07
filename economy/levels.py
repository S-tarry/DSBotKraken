from sqlalchemy import select

from disnake.ext import commands
from database.models import User, Task
from database.requests import assync_session



async def add_xp_to_user_xp(user_id = None, task_id: int = None, bot: commands.Bot = None):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id==user_id))
        task = await session.scalar(select(Task).where(Task.id==task_id))
        user.user_xp += task.xp

        while user.user_xp >= (user.user_level + 1) * 100:
            user.user_level += 1
        
        await session.commit()
        return True
