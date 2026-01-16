from datetime import date
from sqlalchemy import ForeignKey, Numeric, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from decimal import Decimal

class Bookings(Base):

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # связываем с таблицей rooms с помощью foreign key
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    # связываем с таблицей Users
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    date_from: Mapped[date] = mapped_column()
    date_to: Mapped[date] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))
    total_cost: Mapped[Decimal] = mapped_column(Computed("(date_to - date_from) * price"))

    # Обратные связи (чтобы можно было делать booking.user.email)
    user: Mapped["User"] = relationship(back_populates="bookings")
    room: Mapped["Rooms"] = relationship(back_populates="bookings")