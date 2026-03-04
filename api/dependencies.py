from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.orm import Session

from .database import SessionLocal


async def get_db() -> AsyncGenerator[Session, None]:
    with SessionLocal() as session:
        yield session


DBSession = Annotated[Session, Depends(get_db)]
