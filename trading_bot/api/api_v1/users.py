from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.users import UserResponseSchema, UserCreateSchema
from db import db_helper
from db.crud.users import get_all_users, get_user_by_id, create_new_user

router = APIRouter(tags=["Users"])


@router.get("", response_model=list[UserResponseSchema])
async def get_users(session: AsyncSession = Depends(db_helper.session)):
    async with session as session1:
        users = await get_all_users(session=session1)
    import os

    print(os.environ)
    return users


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(user_id: int, session: AsyncSession = Depends(db_helper.session)):
    async with session as session1:
        user = await get_user_by_id(session=session1, user_id=user_id)
    return user


@router.post("", response_model=UserResponseSchema)
async def create_user(
    user_in: UserCreateSchema,
    session: AsyncSession = Depends(db_helper.session),
):

    return await create_new_user(session=session, user_in=user_in)
