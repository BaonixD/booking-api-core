from sqlalchemy import select, and_
from fastapi import HTTPException
from app.models.Hotel import Hotels
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.hotel import HotelCreate

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