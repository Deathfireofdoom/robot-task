from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.crud.result import fetch_all_results
from src.schemas.robot import JobRequest, JobResult
from src.robot.robot import Robot

router = APIRouter()


@router.post("/", response_model=JobResult)
async def post_job(
    request: JobRequest, db: AsyncSession = Depends(get_db_session)
) -> JobResult:
    robot = Robot()

    result = await robot.handle_job(job=request, db=db)

    return result


@router.get("/result", response_model=list[JobResult])
async def get_all_results(db: AsyncSession = Depends(get_db_session)):
    return await fetch_all_results(db)
