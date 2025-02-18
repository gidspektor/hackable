from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel


class Articles(SQLModel, table=True):
    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
