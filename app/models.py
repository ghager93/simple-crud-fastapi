from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field

class Simple(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    number: int
    created_at: datetime
    updated_at: datetime


class SimpleCreate(SQLModel):
    name: str
    number: int


class SimpleOut(SQLModel):
    name: str
    number: int
    created_at: datetime
    updated_at: datetime
