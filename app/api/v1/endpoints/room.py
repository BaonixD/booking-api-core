from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.crud.room import (
    create_room,
    get_rooms_by_hotel,
    get_room_by_id,
    delete_room,
    update_room
)
from app.schemas.room import RoomResponse, RoomCreate, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get( "/hotel/{hotel_id}", response_model=list[RoomResponse] )
async def read_rooms_by_hotel ( hotel_id: int, db: AsyncSession = Depends(get_db) ):
    return await get_rooms_by_hotel( db, hotel_id )
#все комнаты конкретного отеля

@router.get( "/{room_id}", response_model=RoomResponse )
async def read_room_by_id ( room_id: int, db: AsyncSession = Depends(get_db) ):
    return await get_room_by_id( db, room_id )


@router.post( "/create", response_model=RoomResponse )
async def add_room ( room_in: RoomCreate, db: AsyncSession = Depends(get_db) ):
    return await create_room( db, room_in )

@router.delete("/{room_id}")
async def remove_room(room_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_room(db, room_id)

@router.patch( "/{room_id}", response_model=RoomResponse )
async def patch_room( room_id: int, room_in: RoomUpdate, db: AsyncSession = Depends(get_db) ):
    return await update_room( db, room_id, room_in )

















