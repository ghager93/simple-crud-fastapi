from typing import Any, List

from datetime import datetime
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from fastapi.exceptions import HTTPException 

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


@router.get("/simple/{id}", response_model=SimpleOut)
async def get_simple(*, session: Session = Depends(get_session), id: int):
    result = session.query(Simple).filter_by(id=id).first()

    if result:
        return result
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Element not found."
    )