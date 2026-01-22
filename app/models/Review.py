from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base
from datetime import datetime


class Reviews(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column( primary_key=True, nullable=False )
    user_id: Mapped[int] = mapped_column( ForeignKey( "users.id" ), nullable=False )
    hotel_id: Mapped[int] = mapped_column( ForeignKey( "hotels.id" ), nullable=False )
    rating: Mapped[int] = mapped_column( nullable=False )
    comment: Mapped[str] = mapped_column( nullable=False )
    created_at: Mapped[datetime] = mapped_column( default=datetime.now )

    user: Mapped["User"] = relationship(back_populates="reviews")
    hotel: Mapped["Hotels"] = relationship(back_populates="reviews")
