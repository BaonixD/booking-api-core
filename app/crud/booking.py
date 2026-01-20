from sqlalchemy import select, func, and_
from app.models.Booking import Bookings
from app.models.Room import Rooms
from app.schemas.booking import BookingCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.crud.room import get_room_by_id

async def create_booking (session: AsyncSession, booking_data: BookingCreate, user_id: int ):

    # Используем функцию из room
    room = await get_room_by_id( session, booking_data.room_id )


    # Защита от овербукинга. Считаем брони, которые пересекаются по датам
    booking_query = select( func.count() ).select_from(Bookings).where(
        and_(
            Bookings.room_id == booking_data.room_id,
            Bookings.date_from < booking_data.date_to,
            Bookings.date_to > booking_data.date_from
        )
    )
    booking_res = await session.execute(booking_query)
    booked_count = booking_res.scalar()

    if booked_count >= room.quantity:
        raise HTTPException(status_code=400, detail="Свободных номеров нет")


    #создаем бронь
    new_bookings = Bookings(
        room_id = booking_data.room_id,
        user_id=user_id,
        date_from = booking_data.date_from,
        date_to = booking_data.date_to,
        price = room.price
    )

    session.add(new_bookings)
    await session.commit()
    await session.refresh(new_bookings)
    return new_bookings


