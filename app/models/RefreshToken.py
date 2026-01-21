from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.session import Base
from datetime import datetime

class RefreshTokens(Base):

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ondelete="CASCADE" удалит токены, если удалят юзера
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    token: Mapped[str] = mapped_column( unique = True, nullable = False, index = True )
    expires_at: Mapped[datetime] = mapped_column( nullable = False )
    created_at: Mapped[datetime] = mapped_column( default=datetime.now )

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")

