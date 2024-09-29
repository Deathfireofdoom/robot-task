from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.base import add_to_db, query_all, query_by_id
from src.models.result import Result


# create
async def add_result_to_db(db: AsyncSession, result: Result) -> Result:
    return await add_to_db(db, result)


# read
async def fetch_all_results(db: AsyncSession) -> list[Result]:
    return await query_all(db, Result)


async def fetch_result_by_id(db: AsyncSession, result_id: str) -> Result:
    return await query_by_id(db, Result, result_id)
