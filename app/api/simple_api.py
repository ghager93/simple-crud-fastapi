from datetime import datetime
from fastapi import APIRouter

from app.models import SimpleCreate, Simple

router = APIRouter(prefix="/api")


@router.get("/helloworld")
async def hello_world():
    return {"hello world!"}


@router.post("/simple/")
async def create_simple(simple_create: SimpleCreate):
    timestamp = datetime.now()
    simple = Simple(
        name=simple_create.name,
        number=simple_create.number,
        created_at=timestamp,
        updated_at=timestamp
    )
    return simple