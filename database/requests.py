
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import selectinload

from database.models import assync_session
from database.models import User, Role, Task, UserTask, Payout


# add new user and roles into DB
async def add_new_user(user_id: int, username: str, user_card: str, roles: list):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        role_result = await session.scalars(select(Role).where(Role.name.in_(roles)))
        db_roles = role_result.all()
        if not user:
            user = User(user_id=user_id, username=username, user_card=user_card)
            session.add(user)
        for roles in db_roles:
            if roles not in user.roles:
                user.roles.append(roles)
        await session.commit()


# edit user info
async def edit_user_info(user_id: int, username: str, user_card: str, roles: list):
    async with assync_session() as session:
        user_data = (update(User).where(User.user_id==user_id).values(username=username, user_card=user_card))
        await session.execute(user_data)
        if roles:
            result = await session.execute(select(User).options(selectinload(User.roles)).where(User.user_id == user_id))  
            user = result.scalar_one_or_none()

            role_result = await session.scalars(select(Role).where(Role.name.in_(roles)))
            user.roles = role_result.all()
        await session.commit()


# update user info
async def update_user_info(user_id: int):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        user.user_count_task += 1  
        await session.commit()

        
# get user info with DB
async def get_user_info(user_id: int):
    async with assync_session() as session:
        result = await session.execute(select(User).options(selectinload(User.roles)).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        return user


#add tasks into DB
async def add_tasks_into_db(title: str, description: str, status: str, task_priority: str, role: str,  price: int, xp: int):
    async with assync_session() as session:
        task_data = await session.execute(update(Task).where(Task.title==title).values(description=description, status=status, 
                                                                task_priority=task_priority, role=role, price=price, xp=xp))
        if task_data.rowcount == 0:
            await session.execute(insert(Task).values(title=title, description=description, status=status,
                                           task_priority=task_priority, role=role, price=price, xp=xp))
        await session.commit()


# get all tasks with DB
async def get_all_tasks():
    async with assync_session() as session:
        all_tasks = await session.scalars(select(Task))
        return all_tasks.all()


# add tasks for user
async def add_user_tasks(user_id: int, task_id: int):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id==user_id))
        if not user:
            return False
        result = await session.scalar(select(UserTask).where(UserTask.user_id==user.id).where(UserTask.task_id==task_id))
        if result:
            return False
        user_task = UserTask(user_id=user.id, task_id=task_id)
        session.add(user_task)
        await session.commit()
        return True


# update user tasks status and url
async def update_user_tasks(task_id, status: list, task_url: str):
    async with assync_session() as session:
        task = await session.scalar(select(UserTask).where(UserTask.task_id==task_id))
        if not task:
            return False
        
        task.status = status
        if task_url:
            task.task_link = task_url

        await session.commit()
        return True


# get all user tasks for commands - mytasks
async def get_all_user_tasks(user_id):
    async with assync_session() as session:
        result = await session.execute(select(User).options(selectinload(User.tasks)).where(User.user_id==user_id))
        user = result.scalar_one_or_none()
        return user.tasks


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


# clear tables - UserTask, Task, Payout.
async def clear_tables():
    async with assync_session() as session:
        await session.execute(delete(Task))
        await session.execute(delete(UserTask))
        await session.execute(delete(Payout))
        await session.commit()


# get all user how haves pay
async def get_all_user_to_pay():
    async with assync_session() as session:
        user_to_pay = await session.scalars(select(User).where(User.user_balance > 0))
        return user_to_pay


# add transaction info
async def add_payout_info(user_id, amount: int):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        payout = Payout(user_id=user.id, amount=amount)
        session.add(payout)
        user.user_balance = 0
        await session.commit()


# get transaction info
async def get_payout_info():
    async with assync_session() as session:
        all_payout = await session.execute(select(Payout).options(selectinload(Payout.user)))
        return all_payout.scalars().all()