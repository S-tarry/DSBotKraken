import disnake
import os

from disnake.ext import commands
from disnake.ui import Select, View
from disnake import TextInputStyle

from dotenv import load_dotenv
from database.database import get_user_info, edit_user_info
from cogs.config import ROLES, REGIST_ID, NOT_REGIST_ID


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
