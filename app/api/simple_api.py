from fastapi import APIRouter

from app.models import Simple

router = APIRouter(prefix="/api")


@router.get("/helloworld")
async def hello_world():
    return {"hello world!"}


@router.post("/simple/")
async def create_simple(simple: Simple):
    return simple