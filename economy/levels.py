from database.models import User, Task
from database.requests import assync_session
from sqlalchemy import select



async def add_xp_to_user_xp(user_id, task_id: int):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id==user_id))
        task = await session.scalar(select(Task).where(Task.id==task_id))
        level_up = False

        user.user_xp += task.xp

        while user.user_xp >= (user.user_level + 1) * 100:
            user.user_level += 1
            level_up = True
        
        if level_up:
            print(f"User: {user.username} up level")
        
        await session.commit()
        return True
