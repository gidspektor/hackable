from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

from hackable_api.db.models.base import Base


class Articles(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Article(title='{self.title}', id='{self.id}')>"
