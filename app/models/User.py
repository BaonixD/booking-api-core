from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from datetime import datetime



class User(Base):

    __tablename__ = 'users'

    # mapped_column указывает настройки для базы данных
    id: Mapped[int] = mapped_column( primary_key=True, autoincrement=True )
    email: Mapped[str] = mapped_column( unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column( nullable=False)

    firstName: Mapped[str] = mapped_column( nullable=False)
    lastName: Mapped[str] = mapped_column( nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    # cascade="all, delete-orphan" очистит токены, если удалишь юзера
    refresh_tokens: Mapped[list["RefreshTokens"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    reviews: Mapped[list["Reviews"]] = relationship(back_populates="user")