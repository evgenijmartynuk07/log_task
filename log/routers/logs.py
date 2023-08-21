from datetime import datetime
from sqlalchemy import and_, Row, RowMapping
from sqlalchemy.future import select
from fastapi import APIRouter, Depends, Query
from typing import List, Optional, Any, Sequence
from log import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from log.auth.permissions import current_active_user
from log.db.models import DBLog, DBUser
from log.db.engine import get_db
from log.loging_format import process_uploaded_file, process_uploaded_archive

router = APIRouter()


@router.get("/logs/", response_model=List[schemas.Log])
async def get_logs(
        user: DBUser = Depends(current_active_user),
        start_time: Optional[datetime] = Query(
            None,
            description="Start time for filtering. Ex: 2023-10-10 12:38:22"
        ),
        end_time: Optional[datetime] = Query(
            None,
            description="End time for filtering. Ex: 2023-10-10 12:38:22"
        ),
        keywords: Optional[str] = Query(
            None,
            description="Keywords for filtering. Ex: Get, post ect"
        ),
        db: AsyncSession = Depends(get_db)
) -> Sequence[Row | RowMapping | Any]:

    async with db.begin():
        query = select(DBLog)

        if start_time:
            query = query.where(query.timestamp >= start_time)
        if end_time:
            query = query.where(query.timestamp <= end_time)
        if keywords:
            keyword_filters = [
                DBLog.message.ilike(
                    f"%{keyword}%") for keyword in keywords.split()
            ]
            query = query.where(and_(*keyword_filters))

        result = await db.execute(query)
        logs = result.scalars().all()

        return logs


@router.post("/upload_logs/")
async def upload_logs(
        file: schemas.UploadFile,
        db: AsyncSession = Depends(get_db)
) -> dict:

    await process_uploaded_file(file, db)
    return {"message": "Logs uploaded successfully to Database"}


@router.post("/upload_archive/")
async def upload_archive(
        file: schemas.UploadFile,
        db: AsyncSession = Depends(get_db)
) -> dict:

    process = await process_uploaded_archive(file, db)
    return {"message": process}
