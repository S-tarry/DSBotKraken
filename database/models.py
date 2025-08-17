import asyncio
import os

from sqlalchemy import BigInteger, Column, Integer, String, Text, Enum, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv

load_dotenv()

DBPASS = os.getenv('DBPASS')

engine = create_async_engine(url=f"mysql+aiomysql://root:{DBPASS}@localhost:3306/DSBotRKKS")
assync_session = async_sessionmaker(engine)



class Base(AsyncAttrs, DeclarativeBase):
    pass



# таблиця з користувачами
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    user_card: Mapped[str] = mapped_column(String(50), nullable=False)
    user_balance: Mapped[int] = mapped_column(Integer, default=0)
    user_xp: Mapped[int] = mapped_column(Integer, default=0)
    user_level: Mapped[int] = mapped_column(Integer, default=0)
    user_rank: Mapped[str] = mapped_column(String(50), default='None')
    user_count_task: Mapped[int] = mapped_column(Integer, default=0)

    roles: Mapped[list['UserRole']] = relationship('UserRole', back_populates='user')
    tasks: Mapped[list['UserTask']] = relationship('UserTask', back_populates='user')



# таблиця з ролями
class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[list['UserRole']] = relationship('UserRole', back_populates='user')



class UserRole(Base):
    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='roles')
    role: Mapped['Role'] = relationship('Role', back_populates='users')



# таблиця з завданнями
class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Enum("Не розпочато", "Виконується", "Завершено", "Нове", "Оновлене", name="usertask_status_enum"), default="Не розпочато")
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    xp: Mapped[int] = mapped_column(Integer, nullable=False)
    task_priority: Mapped[str] = mapped_column(Enum("Low", "Medium", "High", name="task_priority_enum"), default="Low")



class UserTask(Base):
    __tablename__ = 'usertasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=False)
    status: Mapped[str] = mapped_column(Enum("Не розпочато", "Виконується", "Завершено", "Нове", "Оновлене", name="usertask_status_enum"), default="Не розпочато")
    task_link: Mapped[str] = mapped_column(String(150), nullable=True)
    
    user: Mapped['User'] = relationship('User', back_populates='tasks')
    task: Mapped['Task'] = relationship('Task', back_populates='user_tasks')



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


# asyncio.run(async_main())