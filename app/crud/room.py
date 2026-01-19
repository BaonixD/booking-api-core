from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.Room import Rooms
from app.models.Hotel import Hotels
from app.schemas.room import RoomCreate, RoomUpdate
from fastapi import HTTPException

async def create_room( session: AsyncSession, room_data: RoomCreate ):

# сначала получаем сам отель, потом чекаем его лимит
    hotel_query = select(Hotels).where( Hotels.id == room_data.hotel_id )
    hotel_res = await session.execute(hotel_query)
    hotel = hotel_res.scalars().first() # return 1 object, тот который нам нужен

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")


    # считаем сколько комнат УЖЕ создано для этого Отеля
    # c помощью  func
    count_query = select(func.count()).select_from(Rooms).where(Rooms.hotel_id == room_data.hotel_id) #возвращает конкретное количество созданных комнат определенного отеля
    count_res = await session.execute(count_query)
    current_count = count_res.scalar() # scalar() вернет число напрямую

    if current_count >= hotel.rooms_quantity:
        raise HTTPException(
        status_code=400,
        detail=f"В отеле {hotel.name} может быть не более {hotel.rooms_quantity} типов номеров"
        )

    new_room = Rooms( **room_data.model_dump() )
    session.add(new_room)
    await session.commit()
    await session.refresh(new_room)
    return new_room



async def get_rooms_by_hotel( session: AsyncSession, hotel_id: int ):

    query = select(Rooms).where( Rooms.hotel_id == hotel_id )
    rooms = await session.execute(query)
    return rooms.scalars().all()


async def get_room_by_id(session: AsyncSession, room_id: int):
    query = select(Rooms).where(Rooms.id == room_id)
    res = await session.execute(query)
    room = res.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return room


async def delete_room(session: AsyncSession, room_id: int):
    room = await get_room_by_id(session, room_id)

    await session.delete(room)
    await session.commit()
    return {"message": "Room deleted successfully"}


async def update_room(session: AsyncSession, room_id: int, room_data: RoomUpdate):
    # Ищем комнату
    room = await get_room_by_id(session, room_id)

    # Превращаем схему в словарь
    update_data = room_data.model_dump(exclude_unset=True)

    # Обновляем
    for key, value in update_data.items():
        setattr(room, key, value)

    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room