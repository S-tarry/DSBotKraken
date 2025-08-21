import asyncio
import os

from sqlalchemy import BigInteger, Column, Integer, String, Text, Enum, Float, ForeignKey, DateTime, func, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv

load_dotenv()

DBPASS = os.getenv('DBPASS')

engine = create_async_engine(url=f"mysql+aiomysql://root:{DBPASS}@localhost:3306/DSBotRKKS")
assync_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



class Base(AsyncAttrs, DeclarativeBase):
    pass






# таблиця з користувачами
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    user_card: Mapped[str] = mapped_column(String(50), nullable=False)
    user_balance: Mapped[int] = mapped_column(Integer, default=0)
    user_xp: Mapped[int] = mapped_column(Integer, default=0)
    user_level: Mapped[int] = mapped_column(Integer, default=0)
    user_rank: Mapped[str] = mapped_column(String(50), default='None')
    user_count_task: Mapped[int] = mapped_column(Integer, default=0)

    roles: Mapped[list["Role"]] = relationship(secondary="user_roles", back_populates="users")
    tasks: Mapped[list["Task"]] = relationship(secondary="user_tasks", back_populates="user_tasks")



# таблиця з ролями
class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50))

    users: Mapped[list["User"]] = relationship(secondary="user_roles", back_populates="roles")



class UserRole(Base):
    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id', ondelete="CASCADE"))



# таблиця з завданнями
class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Enum("Не розпочато", "Виконується", "Завершено", "Нове", "Оновлене", name="usertask_status_enum"), default="Не розпочато")
    role: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    xp: Mapped[int] = mapped_column(Integer)
    task_priority: Mapped[str] = mapped_column(Enum("Low", "Medium", "High", name="task_priority_enum"))

    user_tasks: Mapped[list["User"]] = relationship(secondary="user_tasks", back_populates='tasks')



class UserTask(Base):
    __tablename__ = 'user_tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id', ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(Enum("Не розпочато", "Виконується", "Завершено", "Нове", "Оновлене", name="usertask_status_enum"), default="Не розпочато")
    task_link: Mapped[str] = mapped_column(String(150))



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


# asyncio.run(async_main())