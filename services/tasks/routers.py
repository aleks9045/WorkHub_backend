import sys

from fastapi import Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import EmailStr
from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append("../../../GoodProject")

from backend.database import get_async_session
from backend.services.auth.models import UserModel


router = APIRouter(
    prefix="/task",
    tags=["Task"]
)


@router.post('/add', summary="Create new task")
async def create_task(description: str, contact: str,
                      session: AsyncSession = Depends(get_async_session)):
    stmt = insert(UserModel).values(description=description,
                                    contact=contact)
    await session.execute(statement=stmt)
    await session.commit()
    return JSONResponse(status_code=201, content={"detail": "Успешно"})
