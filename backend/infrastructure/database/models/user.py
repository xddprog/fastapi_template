from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.database.models.base import Base

class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)