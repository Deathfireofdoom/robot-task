from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar, List

T = TypeVar("T")


async def query_all(db: AsyncSession, model: Type[T]) -> List[T]:
    stmt = select(model)
    result = await db.execute(stmt)
    return result.scalars().all()


async def query_by_id(db: AsyncSession, model: Type[T], id: str) -> T:
    stmt = select(model).where(model.id == id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def add_to_db(db: AsyncSession, instance: T) -> T:
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance
