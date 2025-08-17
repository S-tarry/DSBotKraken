from sqlalchemy import select, update, delete

from DSBotKraken.database.models import assync_session
from DSBotKraken.database.models import User, Role, UserRole, Task, UserTask


# додає користувача в БД
async def add_new_user(id, name, card, role):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id == id))

        if not user:
            session.add(User(user_id=id, username=name, user_card=card, roles=role))
            await session.commit()