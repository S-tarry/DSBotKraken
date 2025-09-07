import disnake

from disnake.ext import commands
from sqlalchemy import select

from database.models import User
from database.requests import assync_session
from config.config import RANGS


RANGS = {
    0: "новачок",
    8: "учень",
    16: "послідовник",
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


# add new user ranks
async def update_user_rank(user_id: int, bot: commands.Bot = None, guild: disnake.Guild = None):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id==user_id))
        old_rank = user.user_rank
        new_rank = old_rank
        
        for lvl, rank_name in sorted(RANGS.items()):
            if user.user_level >= lvl:
                new_rank = rank_name
        user.user_rank = new_rank
        await session.commit()

    if old_rank != new_rank:
        member = guild.get_member(user_id)
        if member:
            if old_rank and old_rank in RANGS:
                old_role = guild.get_role(RANGS[old_rank])
                if old_rank in member.roles:
                    await member.remove_roles(old_role)
        new_role = guild.get_role(RANGS[new_rank])
        
        if new_rank:
            await member.add_roles(new_role)  

        return old_rank != new_rank
    