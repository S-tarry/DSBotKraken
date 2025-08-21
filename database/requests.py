from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from database.models import assync_session
from database.models import User, Role, UserRole, Task



# add new user and roles into DB
async def add_new_user(user_id: int, username: str, user_card: str, roles: list):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        role_result = await session.scalars(select(Role).where(Role.name.in_(roles)))
        db_roles = role_result.all()
        if not db_roles:
            print("Немає такої ролі в БД")
            return
        if not user:
            user = User(user_id=user_id, username=username, user_card=user_card)
            session.add(user)
        for roles in db_roles:
            if roles not in user.roles:
                user.roles.append(roles)
        await session.commit()


# update user info
async def edit_user_info(user_id: int, username: str, user_card: str, roles: list):
    async with assync_session() as session:
        result = await session.execute(select(User).options(selectinload(User.roles)).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return False

        user.username = username
        user.user_card = user_card

        if roles:
            role_result = await session.scalars(select(Role).where(Role.name.in_(roles)))
            user.roles = role_result.all()

        await session.commit()
        return True
        

# get user info with DB
async def get_user_info(user_id: int):
    async with assync_session() as session:
        result = await session.execute(select(User).options(selectinload(User.roles)).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        return user


#add tasks into DB
async def add_tasks_into_db(title: str, description: str, status: str, price: int, xp: int, task_priority: str):
    async with assync_session() as session:
        new_task = Task(title=title, description=description, status=status, price=price, xp=xp, task_priority=task_priority)
        session.add(new_task)
        await session.commit()



# add all roles into DB
async def add_all_roles_into_db(guild_roles, roles_to_skip: list):
    async with assync_session() as session:
        for role in guild_roles:
            if role.id in roles_to_skip:
                continue

            result = await session.execute(select(Role).where(Role.role_id == role.id))
            existing_role = result.scalar_one_or_none()

            if not existing_role:
                session.add(Role(name=role.name.lower(), role_id=role.id))
        await session.commit()
