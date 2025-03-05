from sqlalchemy import Column, Integer, String, ForeignKey

from app.settings import settings

from db.models.base import Base


class ArticlesComments(Base):
    __tablename__ = "articles_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    comment = Column(String(settings.comment_max_length), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
