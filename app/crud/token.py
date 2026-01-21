from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.RefreshToken import RefreshTokens
from datetime import datetime, timedelta, timezone


async def add_refresh_token( session: AsyncSession, user: int, token: str ):
    now = datetime.now()

    new_token = RefreshTokens(
        user_id = user,
        token = token,
        expires_at= now + timedelta(days=30)
    )

    session.add(new_token)
    await session.commit()

async def get_token_from_db( session: AsyncSession, token_str: str ):

    query = select(RefreshTokens).where( RefreshTokens.token == token_str )
    res = await session.execute(query)
    return res.scalars().first()

async def rotate_refresh_token ( session: AsyncSession, old_token_obj: RefreshTokens ):
    await session.delete(old_token_obj)
    await session.commit()