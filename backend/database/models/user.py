from sqlalchemy.orm import Mapped
from tortoise import fields, models
from backend.database.models.base import Base


class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
