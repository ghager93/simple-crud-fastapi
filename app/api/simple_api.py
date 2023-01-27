from typing import Any, List

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.models import SimpleCreate, Simple, SimpleOut
from app.db import engine, get_session

router = APIRouter(prefix="/api")


@router.get("/helloworld")
async def hello_world():
    return {"hello world!"}


@router.post("/simple/", response_model=SimpleOut)
async def create_simple(*, session: Session = Depends(get_session), simple_create: SimpleCreate):
    timestamp = datetime.now()
    simple = Simple(
        name=simple_create.name,
        number=simple_create.number,
        created_at=timestamp,
        updated_at=timestamp
    )
    
    session.add(simple)
    session.commit()

    return simple


@router.get("/simple/", response_model=List[SimpleOut])
async def get_all_simple(*, session: Session = Depends(get_session)):
    return session.query(Simple).all()