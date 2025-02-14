from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel


class Articles(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str

    __tablename__ = "articles"
