from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.hotels import get_all_hotels, get_hotel_by_id, create_hotel, delete_hotel, update_hotel, get_hotel_full_info
from app.schemas.hotel import HotelResponse, HotelListResponse, HotelCreate, HotelUpdate, HotelWithRoomsResponse


router = APIRouter( prefix="/hotels", tags=["Hotels"] )

@router.get( "/", response_model= list[HotelListResponse] )
async def get_hotels( db: AsyncSession = Depends(get_db) ):
    return await get_all_hotels(db)

@router.get ( "/{hotel_id}", response_model = HotelResponse )
async def read_hotel_by_id ( hotel_id: int, db: AsyncSession = Depends( get_db ) ):

    hotel = await get_hotel_by_id( db, hotel_id )

    if not hotel:
        raise HTTPException ( status_code=404, detail="Hotel not found" )

    return hotel

@router.post( "/create", response_model = HotelResponse )
async def create_hotell( hotel_in: HotelCreate, db: AsyncSession = Depends( get_db ) ):
    hotel = await create_hotel( db, hotel_in )
    return hotel


@router.patch("/{hotel_id}", response_model=HotelResponse)
async def patch_hotel(
    hotel_id: int,
    hotel_in: HotelUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Частичное обновление данных отеля"""
    return await update_hotel(db, hotel_id, hotel_in)

@router.delete("/{hotel_id}")
async def remove_hotel(
    hotel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удаление отеля по ID"""
    return await delete_hotel(db, hotel_id)

@router.get("/{hotel_id}/full", response_model=HotelWithRoomsResponse)
async def read_full_hotel_info(
    hotel_id: int,
    db: AsyncSession = Depends(get_db)
):
    #Возвращает всю информацию об отеле, включая список всех его комнат
    return await get_hotel_full_info(db, hotel_id)
