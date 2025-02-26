from sqlalchemy import Column, Integer, String

from db.models.base import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Integer, default=0)

    def __repr__(self):
        return f"<User(username='{self.username}')>"
