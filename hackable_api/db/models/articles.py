from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
import sqlalchemy as sa

from app.settings import settings

from db.models.base import Base


class Articles(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(settings.title_max_length), nullable=False)
    content = Column(String(settings.article_max_length), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)

    def __repr__(self):
        return f"<Article(title='{self.title}', id='{self.id}')>"
