from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Counter(SQLModel, table=True):
    __tablename__ = "counters"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    value: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CounterCreate(SQLModel, table=False):
    name: str = Field(max_length=100)
    value: int = Field(default=0)


class CounterUpdate(SQLModel, table=False):
    value: Optional[int] = Field(default=None)
