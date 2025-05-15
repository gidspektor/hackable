from sqlalchemy import Column, Integer, String

from hackable_api.db.models.base import Base
from sqlalchemy import Boolean


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    image_name = Column(String(255))
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(username='{self.username}')>"
