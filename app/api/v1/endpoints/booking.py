from fastapi import APIRouter, Depends
from app.schemas.booking import BookingCreate, BookingResponse
from app.crud.booking import create_booking, my_bookings, delete_booking
from app.crud.user import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import User

router = APIRouter( prefix="/bookings", tags=["Bookings"] )

@router.post( "/create", response_model= BookingResponse )
async def add_bookings ( booking_in: BookingCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user) ):
    return await create_booking( db, booking_in, user.id )

@router.get( "/my", response_model=list[BookingResponse] )
async def get_my_bookings ( db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user) ):
    return await my_bookings( db, user.id )


@router.delete ( "/delete/{booking_id}" )
async def delete_bookings ( booking_id: int, db: AsyncSession = Depends(get_db),user: User = Depends(get_current_user) ):
    return await delete_booking( db, booking_id, user.id )