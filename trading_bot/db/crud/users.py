from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.users import UserCreateSchema
from db import User


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    # result = await session.execute(stmt)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    user = await session.scalar(stmt)
    return user


async def create_new_user(session: AsyncSession, user_in: UserCreateSchema) -> User:
    user = User(**user_in.dict())
    async with session as session1:
        session1.add(user)
    return user
