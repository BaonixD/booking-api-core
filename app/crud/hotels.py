from sqlalchemy import select, and_, func
from fastapi import HTTPException
from app.models.Hotel import Hotels
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.hotel import HotelCreate, HotelUpdate
from sqlalchemy.orm import selectinload
from app.models.Room import Rooms
from app.models.Booking import Bookings
from datetime import date

async def get_all_hotels( session: AsyncSession ):

    # получаем все hotels
    query = select(Hotels)
    res = await session.execute(query)
    return res.scalars().all() #возвращает объекты классов (экземпляр моделей Hotel)

async def get_hotel_by_id ( session: AsyncSession, hotel_id: int ):

    query = select(Hotels).where( Hotels.id == hotel_id )
    res = await session.execute(query)
    return res.scalars().first() # возвращает только один объект

async def create_hotel ( session: AsyncSession, hotel_data: HotelCreate ):

    query = select(Hotels).where( and_( Hotels.name == hotel_data.name, Hotels.location == hotel_data.location ) )
    res = await session.execute(query)


    existing_hotel = res.scalars().first()

    # проверка есть ли такой отель. existing hotel возвращает 1 or 0
    if existing_hotel:
        raise HTTPException ( status_code=400, detail="Hotel already exist" )


    # Pydantic превращяем в словарь
    new_hotel = Hotels( **hotel_data.model_dump() )
    session.add(new_hotel)
    await session.commit()
    await session.refresh(new_hotel)
    return new_hotel


async def delete_hotel(session: AsyncSession, hotel_id: int):
    """Удаление отеля"""
    hotel = await get_hotel_by_id(session, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    await session.delete(hotel)
    await session.commit()
    return {"message": f"Hotel {hotel_id} deleted successfully"}


async def update_hotel(session: AsyncSession, hotel_id: int, hotel_data: HotelUpdate):
    """Обновление данных отеля"""
    hotel = await get_hotel_by_id(session, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    # Превращаем схему в словарь, игнорируя непереданные поля
    update_data = hotel_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(hotel, key, value)

    session.add(hotel)
    await session.commit()
    await session.refresh(hotel)
    return hotel


async def get_hotel_full_info(session: AsyncSession, hotel_id: int):
    # Запрашиваем отель и просим сразу загрузить список его комнат
    query = (
        select(Hotels)
        .options(selectinload(Hotels.rooms))
        .where(Hotels.id == hotel_id)
    )

    result = await session.execute(query)
    hotel = result.scalars().first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")

    return hotel

async def search_hotels_by_availability( session: AsyncSession, location: str, date_from: date, date_to: date ):

    booked_rooms = select(
        Bookings.room_id,
        func.count( Bookings.id ).label( "booked_count" )
    ).where(
        and_(
            Bookings.date_from < date_to,
            Bookings.date_to > date_from
        )
    ).group_by( Bookings.room_id ).cte("booked_rooms")

    # объединяем отели и комнаты, вычитая брони
    query = (
        select(
            Hotels.id,
            Hotels.name,
            Hotels.location,
            Hotels.stars,
            (func.sum(Rooms.quantity) - func.sum(func.coalesce(booked_rooms.c.booked_count, 0))).label("rooms_left")
        )
        .join(Rooms, Rooms.hotel_id == Hotels.id)
        .outerjoin(booked_rooms, booked_rooms.c.room_id == Rooms.id)
        .where(Hotels.location.icontains(location))
        .group_by(Hotels.id)
        .having(func.sum(Rooms.quantity) - func.sum(func.coalesce(booked_rooms.c.booked_count, 0)) > 0)
    )

    result = await session.execute(query)
    return result.mappings().all()