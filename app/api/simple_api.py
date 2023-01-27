from fastapi import APIRouter

from app.models import SimpleCreate

router = APIRouter(prefix="/api")


@router.get("/helloworld")
async def hello_world():
    return {"hello world!"}


@router.post("/simple/")
async def create_simple(simple: SimpleCreate):
    return simple