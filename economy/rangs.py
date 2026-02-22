import disnake
import logging

from disnake.ext import commands
from sqlalchemy import select

from database.models import User
from database.requests import assync_session
from config.config import RANGS, SERVER_ID


RANGS_LEVELS = {
    0: "новачок",
    8: "учень",
    16: "адепт",
    24: "практик",
    32: "майстер",
    40: "експерт",
    48: "профі",
    56: "винахідник",
    64: "творець",
    72: "магістр",
    84: "легенда",
    100: "гуру",
}



async def update_user_rank(user_id: int, bot: commands.Bot):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        old_rank = user.user_rank
        new_rank = old_rank
        guild = bot.get_guild(SERVER_ID)

        # Визначаємо новий ранг на основі рівня
        for lvl, rank_name in sorted(RANGS_LEVELS.items()):
            if user.user_level >= lvl:
                new_rank = rank_name

        user.user_rank = new_rank
        await session.commit()

    if old_rank != new_rank:
        member = guild.get_member(user_id)
        if not member:
            logging.warning(f"❌ Не знайшов учасника {user_id} у гільдії {guild.name}")
            return False

        # Прибираємо стару роль
        if old_rank and old_rank in RANGS:
            old_role = guild.get_role(RANGS[old_rank])
            if old_role and old_role in member.roles:
                await member.remove_roles(old_role)
                logging.info(f"🔻 Прибрав роль {old_rank} у {member.display_name}")
        elif old_rank:
            logging.warning(f"⚠️ Для рангу '{old_rank}' немає ID у RANGS")

        # Додаємо нову роль
        if new_rank and new_rank in RANGS:
            new_role = guild.get_role(RANGS[new_rank])
            if new_role and new_role not in member.roles:
                await member.add_roles(new_role)
                logging.info(f"✅ Видана роль {new_rank} користувачу {member.display_name}")
        else:
            logging.warning(f"⚠️ Для рангу '{new_rank}' немає ID у RANGS")

        return True

    return False


# # add new user ranks
# async def update_user_rank(user_id: int, bot: commands.Bot = None):
#     async with assync_session() as session:
#         user = await session.scalar(select(User).where(User.user_id==user_id))
#         old_rank = user.user_rank
#         new_rank = old_rank
#         guild = bot.get_guild(SERVER_ID)
        
#         for lvl, rank_name in sorted(RANGS_LEVELS.items()):
#             if user.user_level >= lvl:
#                 new_rank = rank_name

#         user.user_rank = new_rank
#         await session.commit()

#     if old_rank != new_rank:
#         member = guild.get_member(user_id)
#         if not member:
#             return
#         if old_rank and old_rank in RANGS:
#             old_role = guild.get_role(RANGS[old_rank])
#             if old_role and old_role in member.roles:
#                 await member.remove_roles(old_role)
#                 print("Rank: ", old_rank, "Role", old_role)

#         if new_rank and new_rank in RANGS:
#             new_role = guild.get_role(RANGS[new_rank])
#             if new_role and new_role not in member.roles:
#                 await member.add_roles(new_role)
#                 print("New Role: ", new_role)

#         return True
    