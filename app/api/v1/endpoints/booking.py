from fastapi import APIRouter, Depends
from app.schemas.booking import BookingCreate, BookingResponse
from app.crud.booking import create_booking
from app.crud.user import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import User

router = APIRouter( prefix="/bookings", tags=["Bookings"] )

@router.post( "/create", response_model= BookingResponse )
async def add_bookings ( booking_in: BookingCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user) ):
    return await create_booking( db, booking_in, user.id )

