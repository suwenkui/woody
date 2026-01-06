from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from . import models, schemas, auth

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def get_user_count(db: AsyncSession):
    result = await db.execute(select(func.count(models.User.id)))
    return result.scalar()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_apis(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.ApiInfo).offset(skip).limit(limit))
    return result.scalars().all()

async def get_api_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(models.ApiInfo).filter(models.ApiInfo.name == name))
    return result.scalars().first()

async def get_api(db: AsyncSession, api_id: int):
    result = await db.execute(select(models.ApiInfo).filter(models.ApiInfo.id == api_id))
    return result.scalars().first()

async def create_api(db: AsyncSession, api: schemas.ApiInfoCreate):
    db_api = models.ApiInfo(**api.dict())
    db.add(db_api)
    await db.commit()
    await db.refresh(db_api)
    return db_api
