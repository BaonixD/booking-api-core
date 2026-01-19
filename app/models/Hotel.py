from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from sqlalchemy import JSON, UniqueConstraint


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)

    services: Mapped[list[str]] = mapped_column(JSON, nullable=True) # Postgres поймет это как JSON
    stars: Mapped[int] = mapped_column(nullable=True)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column(nullable=True)

    # Связь: у одного отеля много номеров
    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

    # Это ограничение не даст вставить в базу отель с тем же именем И адресом
    __table_args__ = (
        UniqueConstraint("name", "location", name="uq_hotels_name_location"),
    )