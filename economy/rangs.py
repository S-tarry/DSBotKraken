from database.models import User
from database.requests import assync_session
from sqlalchemy import select


RANGS = {
    0: "Новачок",
    1: "Учень"
}


# add new user ranks
async def update_user_rank(user_id: int):
    async with assync_session() as session:
        user = await session.scalar(select(User).where(User.user_id==user_id))
        old_rank = user.user_rank
        new_rank = old_rank
        
        for lvl, rank_name in sorted(RANGS.items()):
            if user.user_level >= lvl:
                new_rank = rank_name
        user.user_rank = new_rank 
        
        await session.commit()
        return old_rank != new_rank
    