from database.models import User, Task
from database.requests import assync_session
from sqlalchemy import select



async def add_money_to_balance(user_id, task_id: int):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id==user_id))
        task = await session.scalar(select(Task).where(Task.id==task_id))

        user.user_balance += task.price

        await session.commit()
        return True

