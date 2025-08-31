import disnake
import os

from disnake.ext import commands
from disnake.ui import Select, View
from disnake import TextInputStyle

from dotenv import load_dotenv
from database.database import get_user_info, edit_user_info
from config.config import ROLES, REGIST_ID, NOT_REGIST_ID, PRIORITY_COLORS


# embeds with user info
def registration_confirm_embed(username: str, bank_card: str, roles: list[str]):
    roles_text = ", ".join(roles)
    embed = disnake.Embed(
        title="Підтвердити інформацію?",
        color=disnake.Color.blue()
    )
    embed.add_field(name="Ім'я", value=username, inline=False)
    embed.add_field(name="Картка", value=bank_card, inline=False)
    embed.add_field(name="Ролі", value=roles_text, inline=False)
    return embed

# embeds with tasks info
def tasks_info_embed(id: int, title: str, description: str, status: str, task_priority: str, role: str, price: int, xp: int ):
    embed = disnake.Embed(
        title=f"{id}) {title} 🏷️",
        description=f"{description}",
        color=PRIORITY_COLORS.get(task_priority, disnake.Color.greyple())
    )
    embed.add_field(name="Статус ✅", value=status, inline=True)
    embed.add_field(name="Пріоритет ⚡", value=task_priority, inline=True)
    embed.add_field(name="Роль 👤", value=role, inline=False)
    embed.add_field(name="Ціна 💰", value=price, inline=True)
    embed.add_field(name="Досвід 🎓", value=xp, inline=True)
    return embed

# embeds with pay user info
def pay_info_embed(username: str, bank_card: int, amount: int, task_complated: int):
    embed = disnake.Embed(
        title=f"Виплата користувачу - {username}",
        color=disnake.Color.blurple()
    )
    embed.add_field(name="Ім'я користувача", value=username, inline=True)
    embed.add_field(name="Карта", value=bank_card, inline=False)
    embed.add_field(name="Сума", value=amount, inline=True)
    embed.add_field(name="Кількість виконаних завдань", value=task_complated, inline=True)
    return embed


